package com.azyan.music.data

import android.content.Context
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.json.Json
import java.io.File
import java.util.UUID

/**
 * Tiny JSON-backed store for favourites, playlists and the last playback session.
 *
 * Deliberately avoids Room/KSP: one small file, written with a short debounce.
 */
object LibraryStore {

    private const val TAG = "LibraryStore"
    private const val FILE_NAME = "azyan_music_store.json"
    private const val WRITE_DEBOUNCE_MS = 400L

    private val json = Json {
        ignoreUnknownKeys = true
        encodeDefaults = true
    }
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    private var writeJob: Job? = null
    private var storeFile: File? = null

    private val _data = MutableStateFlow(LibraryStoreData())
    val data: StateFlow<LibraryStoreData> = _data.asStateFlow()

    fun init(context: Context) {
        if (storeFile != null) return
        val file = File(context.applicationContext.filesDir, FILE_NAME)
        storeFile = file
        if (file.exists()) {
            _data.value = runCatching {
                json.decodeFromString(LibraryStoreData.serializer(), file.readText())
            }.getOrElse { error ->
                Log.w(TAG, "Gagal membaca penyimpanan, mulai kosong", error)
                LibraryStoreData()
            }
        }
    }

    // --- Favourites ---------------------------------------------------------

    fun toggleFavorite(song: Song) {
        update { current ->
            val alreadySaved = current.favorites.any { it.id == song.id }
            current.copy(
                favorites = if (alreadySaved) {
                    current.favorites.filterNot { it.id == song.id }
                } else {
                    current.favorites + song.toSavedSong()
                }
            )
        }
    }

    // --- Playlists ----------------------------------------------------------

    fun createPlaylist(name: String): String {
        val id = UUID.randomUUID().toString()
        val cleanName = name.trim().ifBlank { "Playlist baru" }
        update { current ->
            current.copy(playlists = current.playlists + Playlist(id = id, name = cleanName))
        }
        return id
    }

    fun deletePlaylist(id: String) {
        update { current ->
            current.copy(playlists = current.playlists.filterNot { it.id == id })
        }
    }

    fun addSongsToPlaylist(id: String, songs: List<Song>) {
        if (songs.isEmpty()) return
        update { current ->
            current.copy(
                playlists = current.playlists.map { playlist ->
                    if (playlist.id != id) {
                        playlist
                    } else {
                        val existingIds = playlist.songs.map { it.id }.toSet()
                        val additions = songs
                            .filterNot { it.id in existingIds }
                            .map { it.toSavedSong() }
                        playlist.copy(songs = playlist.songs + additions)
                    }
                }
            )
        }
    }

    fun removeSongFromPlaylist(id: String, songId: Long) {
        update { current ->
            current.copy(
                playlists = current.playlists.map { playlist ->
                    if (playlist.id != id) {
                        playlist
                    } else {
                        playlist.copy(songs = playlist.songs.filterNot { it.id == songId })
                    }
                }
            )
        }
    }

    // --- Last playback session ---------------------------------------------

    fun savePlayback(
        queue: List<Song>,
        index: Int,
        positionMs: Long,
        shuffle: Boolean,
        repeatMode: Int
    ) {
        update { current ->
            current.copy(
                lastQueue = queue.map { it.toSavedSong() },
                lastIndex = index,
                lastPositionMs = positionMs,
                lastShuffle = shuffle,
                lastRepeatMode = repeatMode
            )
        }
    }

    // --- Persistence --------------------------------------------------------

    private fun update(transform: (LibraryStoreData) -> LibraryStoreData) {
        _data.update(transform)
        scheduleWrite()
    }

    private fun scheduleWrite() {
        val file = storeFile ?: return
        writeJob?.cancel()
        writeJob = scope.launch {
            delay(WRITE_DEBOUNCE_MS)
            val payload = json.encodeToString(LibraryStoreData.serializer(), _data.value)
            runCatching { file.writeText(payload) }
                .onFailure { Log.e(TAG, "Gagal menyimpan pustaka", it) }
        }
    }
}
