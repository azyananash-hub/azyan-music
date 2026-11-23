package com.azyan.music.ui.library.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.MusicNote
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.azyan.music.data.MediaStoreScanner
import com.azyan.music.data.Song

/**
 * Album art with a deterministic fallback.
 *
 * Layer bawah: gradasi yang dibuat dari hash judul + artis. Lagu yang sama
 * selalu mendapat gradasi yang sama, dan tidak memakai aset pihak ketiga.
 * Layer atas: cover dari MediaStore (jika ada). Jika gambar gagal dimuat,
 * gradasi tetap terlihat.
 */
@Composable
fun SongArtwork(
    song: Song,
    modifier: Modifier = Modifier,
    cornerRadius: Dp = 10.dp
) {
    val gradient = remember(song.title, song.artist) { fallbackGradient(song.title, song.artist) }

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(cornerRadius))
            .background(gradient),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = Icons.Rounded.MusicNote,
            contentDescription = null,
            tint = Color.White.copy(alpha = 0.85f),
            modifier = Modifier.fillMaxSize(0.45f)
        )
        if (song.albumId > 0L) {
            AsyncImage(
                model = MediaStoreScanner.albumArtUri(song.albumId),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

/**
 * Dua warna dengan hue berbeda dari hash, saturasi dan kecerahan dibatasi
 * agar tetap kalem di tema gelap. Hasilnya deterministik.
 */
internal fun fallbackGradient(title: String, artist: String): Brush {
    val hash = (title + "\u0000" + artist).hashCode()
    val hue = Math.floorMod(hash, 360).toFloat()
    val hueSecond = (hue + 40f) % 360f
    val start = hsvColor(hue, saturation = 0.55f, value = 0.42f)
    val end = hsvColor(hueSecond, saturation = 0.45f, value = 0.22f)
    return Brush.linearGradient(colors = listOf(start, end))
}

private fun hsvColor(hue: Float, saturation: Float, value: Float): Color =
    Color(android.graphics.Color.HSVToColor(floatArrayOf(hue, saturation, value)))
