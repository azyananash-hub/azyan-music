package com.azyan.music.playback

import android.content.ComponentName
import android.content.Context
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import androidx.media3.session.SessionToken
import com.azyan.music.data.Song
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class PlayerUiState(
    val currentSong: Song? = null,
    val isPlaying: Boolean = false,
    val positionMs: Long = 0L,
    val durationMs: Long = 0L,
    val hasNext: Boolean = false,
    val hasPrevious: Boolean = false,
    val isShuffling: Boolean = false,
    val repeatMode: Int = Player.REPEAT_MODE_OFF
)

/**
 * UI-side connection to [MusicService] through a [MediaController].
 * All playback commands go through the service, so playback survives the
 * activity being destroyed.
 */
object PlayerController {

    private const val TAG = "PlayerController"
    private const val TICK_MS = 500L

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private var ticker: Job? = null

    private var controller: MediaController? = null
    private var connecting = false
    private var pendingAction: ((MediaController) -> Unit)? = null

    private val _state = MutableStateFlow(PlayerUiState())
    val state: StateFlow<PlayerUiState> = _state.asStateFlow()

    private val listener = object : Player.Listener {
        override fun onEvents(player: Player, events: Player.Events) {
            if (player.isPlaying) startTicker() else stopTicker()
            publish()
        }
    }

    fun connect(context: Context) {
        if (controller != null || connecting) return
        connecting = true

        val appContext = context.applicationContext
        val token = SessionToken(appContext, ComponentName(appContext, MusicService::class.java))
        val future = MediaController.Builder(appContext, token).buildAsync()

        future.addListener({
            connecting = false
            try {
                val connected = future.get()
                controller = connected
                connected.addListener(listener)
                pendingAction?.invoke(connected)
                pendingAction = null
                publish()
            } catch (e: Exception) {
                Log.e(TAG, "Gagal terhubung ke MusicService", e)
            }
        }, ContextCompat.getMainExecutor(appContext))
    }

    fun play(context: Context, songs: List<Song>, startIndex: Int) {
        if (songs.isEmpty()) return
        PlaybackQueue.set(songs)
        val index = startIndex.coerceIn(0, songs.lastIndex)

        withController(context) { player ->
            player.setMediaItems(songs.map { it.toMediaItem() }, index, 0L)
            player.prepare()
            player.play()
        }
    }

    fun togglePlayPause() {
        val player = controller ?: return
        if (player.isPlaying) player.pause() else player.play()
    }

    fun next() {
        controller?.seekToNextMediaItem()
    }

    fun previous() {
        val player = controller ?: return
        if (player.currentPosition > 3_000L) {
            player.seekTo(0L)
        } else if (player.hasPreviousMediaItem()) {
            player.seekToPreviousMediaItem()
        } else {
            player.seekTo(0L)
        }
    }

    fun seekTo(positionMs: Long) {
        controller?.seekTo(positionMs.coerceAtLeast(0L))
    }

    fun toggleShuffle() {
        val player = controller ?: return
        player.shuffleModeEnabled = !player.shuffleModeEnabled
    }

    fun cycleRepeatMode() {
        val player = controller ?: return
        player.repeatMode = when (player.repeatMode) {
            Player.REPEAT_MODE_OFF -> Player.REPEAT_MODE_ALL
            Player.REPEAT_MODE_ALL -> Player.REPEAT_MODE_ONE
            else -> Player.REPEAT_MODE_OFF
        }
    }

    private fun withController(context: Context, action: (MediaController) -> Unit) {
        val player = controller
        if (player != null) {
            action(player)
            return
        }
        pendingAction = action
        connect(context)
    }

    private fun publish() {
        val player = controller ?: return
        val song = PlaybackQueue.songs.value.getOrNull(player.currentMediaItemIndex)
        val duration = player.duration.takeIf { it > 0L } ?: song?.durationMs ?: 0L

        _state.value = PlayerUiState(
            currentSong = song,
            isPlaying = player.isPlaying,
            positionMs = player.currentPosition.coerceAtLeast(0L),
            durationMs = duration,
            hasNext = player.hasNextMediaItem(),
            hasPrevious = player.hasPreviousMediaItem(),
            isShuffling = player.shuffleModeEnabled,
            repeatMode = player.repeatMode
        )
    }

    private fun startTicker() {
        if (ticker?.isActive == true) return
        ticker = scope.launch {
            while (true) {
                publish()
                delay(TICK_MS)
            }
        }
    }

    private fun stopTicker() {
        ticker?.cancel()
        ticker = null
    }
}
