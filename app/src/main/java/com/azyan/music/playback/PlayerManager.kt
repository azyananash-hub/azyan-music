package com.azyan.music.playback

import android.content.Context
import androidx.media3.common.AudioAttributes
import androidx.media3.common.MediaItem
import androidx.media3.common.MediaMetadata
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
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
 * Application-scoped ExoPlayer holder.
 *
 * Phase 1 keeps playback inside the process; Phase 2 moves this into a
 * MediaSessionService so it keeps running in the background.
 */
object PlayerManager {

    private const val TICK_MS = 500L

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private var ticker: Job? = null
    private var exoPlayer: ExoPlayer? = null
    private var queue: List<Song> = emptyList()

    private val _state = MutableStateFlow(PlayerUiState())
    val state: StateFlow<PlayerUiState> = _state.asStateFlow()

    private fun ensurePlayer(context: Context): ExoPlayer {
        exoPlayer?.let { return it }

        val created = ExoPlayer.Builder(context.applicationContext)
            .setAudioAttributes(AudioAttributes.DEFAULT, true)
            .setHandleAudioBecomingNoisy(true)
            .build()

        created.addListener(object : Player.Listener {
            override fun onIsPlayingChanged(isPlaying: Boolean) {
                if (isPlaying) startTicker() else stopTicker()
                publish()
            }

            override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int) {
                publish()
            }

            override fun onPlaybackStateChanged(playbackState: Int) {
                publish()
            }

            override fun onRepeatModeChanged(repeatMode: Int) {
                publish()
            }

            override fun onShuffleModeEnabledChanged(shuffleModeEnabled: Boolean) {
                publish()
            }
        })

        exoPlayer = created
        return created
    }

    fun play(context: Context, songs: List<Song>, startIndex: Int) {
        if (songs.isEmpty()) return
        val player = ensurePlayer(context)
        queue = songs
        player.setMediaItems(
            songs.map { it.toMediaItem() },
            startIndex.coerceIn(0, songs.lastIndex),
            0L
        )
        player.prepare()
        player.play()
        publish()
    }

    fun togglePlayPause() {
        val player = exoPlayer ?: return
        if (player.isPlaying) {
            player.pause()
        } else {
            if (player.playbackState == Player.STATE_IDLE) player.prepare()
            player.play()
        }
    }

    fun next() {
        exoPlayer?.seekToNextMediaItem()
    }

    fun previous() {
        val player = exoPlayer ?: return
        if (player.currentPosition > 3_000L) {
            player.seekTo(0L)
        } else if (player.hasPreviousMediaItem()) {
            player.seekToPreviousMediaItem()
        } else {
            player.seekTo(0L)
        }
    }

    fun seekTo(positionMs: Long) {
        exoPlayer?.seekTo(positionMs.coerceAtLeast(0L))
    }

    fun toggleShuffle() {
        val player = exoPlayer ?: return
        player.shuffleModeEnabled = !player.shuffleModeEnabled
    }

    fun cycleRepeatMode() {
        val player = exoPlayer ?: return
        player.repeatMode = when (player.repeatMode) {
            Player.REPEAT_MODE_OFF -> Player.REPEAT_MODE_ALL
            Player.REPEAT_MODE_ALL -> Player.REPEAT_MODE_ONE
            else -> Player.REPEAT_MODE_OFF
        }
    }

    fun release() {
        stopTicker()
        exoPlayer?.release()
        exoPlayer = null
        queue = emptyList()
        _state.value = PlayerUiState()
    }

    private fun publish() {
        val player = exoPlayer ?: return
        val song = queue.getOrNull(player.currentMediaItemIndex)
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

    private fun Song.toMediaItem(): MediaItem =
        MediaItem.Builder()
            .setUri(uri)
            .setMediaId(id.toString())
            .setMediaMetadata(
                MediaMetadata.Builder()
                    .setTitle(title)
                    .setArtist(artist)
                    .setAlbumTitle(album)
                    .build()
            )
            .build()
}
