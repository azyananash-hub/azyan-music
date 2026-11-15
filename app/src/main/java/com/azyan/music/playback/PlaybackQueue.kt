package com.azyan.music.playback

import android.net.Uri
import androidx.media3.common.MediaItem
import androidx.media3.common.MediaMetadata
import com.azyan.music.data.MediaStoreScanner
import com.azyan.music.data.Song
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * In-memory queue shared between the UI process and [MusicService].
 * Both live in the same process, so a plain singleton is enough.
 */
object PlaybackQueue {

    private val _songs = MutableStateFlow<List<Song>>(emptyList())
    val songs: StateFlow<List<Song>> = _songs.asStateFlow()

    fun set(songs: List<Song>) {
        _songs.value = songs
    }
}

fun Song.toMediaItem(): MediaItem {
    val artwork: Uri? = if (albumId > 0L) MediaStoreScanner.albumArtUri(albumId) else null
    return MediaItem.Builder()
        .setUri(uri)
        .setMediaId(id.toString())
        .setMediaMetadata(
            MediaMetadata.Builder()
                .setTitle(title)
                .setArtist(artist)
                .setAlbumTitle(album)
                .setArtworkUri(artwork)
                .build()
        )
        .build()
}
