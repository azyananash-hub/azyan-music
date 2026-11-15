package com.azyan.music.data

import android.net.Uri

/**
 * One audio track found in the device media library.
 */
data class Song(
    val id: Long,
    val title: String,
    val artist: String,
    val album: String,
    val albumId: Long,
    val durationMs: Long,
    val folder: String,
    val uri: Uri
)
