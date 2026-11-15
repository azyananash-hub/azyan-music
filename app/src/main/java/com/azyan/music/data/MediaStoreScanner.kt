package com.azyan.music.data

import android.content.ContentUris
import android.content.Context
import android.net.Uri
import android.os.Build
import android.provider.MediaStore
import android.util.Log

/**
 * Reads audio files from [MediaStore]. No database of our own is kept: MediaStore
 * is the single source of truth for the library.
 */
object MediaStoreScanner {

    private const val TAG = "MediaStoreScanner"
    private const val MIN_DURATION_MS = 10_000L
    private const val UNKNOWN_ARTIST = "Artis tidak diketahui"
    private const val UNKNOWN_ALBUM = "Album tidak diketahui"
    private const val UNKNOWN_FOLDER = "Lainnya"

    private val collection: Uri
        get() = MediaStore.Audio.Media.EXTERNAL_CONTENT_URI

    /**
     * Blocking scan, call from a background dispatcher.
     *
     * @return songs sorted by title, or an empty list when permission is missing.
     */
    @Suppress("DEPRECATION")
    fun scan(context: Context): List<Song> {
        val projection = mutableListOf(
            MediaStore.Audio.Media._ID,
            MediaStore.Audio.Media.TITLE,
            MediaStore.Audio.Media.ARTIST,
            MediaStore.Audio.Media.ALBUM,
            MediaStore.Audio.Media.ALBUM_ID,
            MediaStore.Audio.Media.DURATION,
            MediaStore.Audio.Media.DATA
        )
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            projection.add(MediaStore.Audio.Media.BUCKET_DISPLAY_NAME)
        }

        val selection = "${MediaStore.Audio.Media.IS_MUSIC} != 0"
        val songs = ArrayList<Song>()

        try {
            context.contentResolver
                .query(collection, projection.toTypedArray(), selection, null, null)
                ?.use { cursor ->
                    val idIndex = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media._ID)
                    val titleIndex = cursor.getColumnIndex(MediaStore.Audio.Media.TITLE)
                    val artistIndex = cursor.getColumnIndex(MediaStore.Audio.Media.ARTIST)
                    val albumIndex = cursor.getColumnIndex(MediaStore.Audio.Media.ALBUM)
                    val albumIdIndex = cursor.getColumnIndex(MediaStore.Audio.Media.ALBUM_ID)
                    val durationIndex = cursor.getColumnIndex(MediaStore.Audio.Media.DURATION)
                    val dataIndex = cursor.getColumnIndex(MediaStore.Audio.Media.DATA)
                    val bucketIndex = cursor.getColumnIndex(MediaStore.Audio.Media.BUCKET_DISPLAY_NAME)

                    while (cursor.moveToNext()) {
                        val duration = cursor.longOrZero(durationIndex)
                        if (duration < MIN_DURATION_MS) continue

                        val id = cursor.getLong(idIndex)
                        val dataPath = cursor.stringOrEmpty(dataIndex)
                        val folder = cursor.stringOrEmpty(bucketIndex)
                            .ifBlank { dataPath.substringBeforeLast('/', "").substringAfterLast('/') }
                            .ifBlank { UNKNOWN_FOLDER }

                        songs.add(
                            Song(
                                id = id,
                                title = cursor.stringOrEmpty(titleIndex).ifBlank { "Tanpa judul" },
                                artist = cursor.stringOrEmpty(artistIndex)
                                    .takeUnless { it.isBlank() || it == "<unknown>" }
                                    ?: UNKNOWN_ARTIST,
                                album = cursor.stringOrEmpty(albumIndex)
                                    .takeUnless { it.isBlank() || it == "<unknown>" }
                                    ?: UNKNOWN_ALBUM,
                                albumId = cursor.longOrZero(albumIdIndex),
                                durationMs = duration,
                                folder = folder,
                                uri = ContentUris.withAppendedId(collection, id)
                            )
                        )
                    }
                }
        } catch (e: SecurityException) {
            Log.w(TAG, "Tidak punya izin membaca MediaStore", e)
            return emptyList()
        } catch (e: Exception) {
            Log.e(TAG, "Gagal memindai MediaStore", e)
            return emptyList()
        }

        return songs.sortedWith(compareBy(String.CASE_INSENSITIVE_ORDER) { it.title })
    }

    /** Legacy album-art content uri understood by Coil; falls back gracefully when missing. */
    fun albumArtUri(albumId: Long): Uri =
        ContentUris.withAppendedId(Uri.parse("content://media/external/audio/albumart"), albumId)
}

private fun android.database.Cursor.stringOrEmpty(index: Int): String =
    if (index >= 0 && !isNull(index)) getString(index) ?: "" else ""

private fun android.database.Cursor.longOrZero(index: Int): Long =
    if (index >= 0 && !isNull(index)) getLong(index) else 0L
