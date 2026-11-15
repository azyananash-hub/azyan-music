package com.azyan.music.data

import android.net.Uri
import kotlinx.serialization.Serializable

/**
 * Snapshot of a song stored on disk. Keeping the metadata (not just the MediaStore id)
 * means playlists and favourites survive a media re-index or a temporarily removed file.
 */
@Serializable
data class SavedSong(
    val id: Long,
    val title: String,
    val artist: String,
    val album: String,
    val albumId: Long = 0L,
    val durationMs: Long = 0L,
    val folder: String = "",
    val uri: String
)

@Serializable
data class Playlist(
    val id: String,
    val name: String,
    val songs: List<SavedSong> = emptyList()
)

@Serializable
data class LibraryStoreData(
    val favorites: List<SavedSong> = emptyList(),
    val playlists: List<Playlist> = emptyList(),
    val lastQueue: List<SavedSong> = emptyList(),
    val lastIndex: Int = 0,
    val lastPositionMs: Long = 0L,
    val lastShuffle: Boolean = false,
    val lastRepeatMode: Int = 0
)

fun Song.toSavedSong(): SavedSong = SavedSong(
    id = id,
    title = title,
    artist = artist,
    album = album,
    albumId = albumId,
    durationMs = durationMs,
    folder = folder,
    uri = uri.toString()
)

fun SavedSong.toSong(): Song = Song(
    id = id,
    title = title,
    artist = artist,
    album = album,
    albumId = albumId,
    durationMs = durationMs,
    folder = folder,
    uri = Uri.parse(uri)
)
