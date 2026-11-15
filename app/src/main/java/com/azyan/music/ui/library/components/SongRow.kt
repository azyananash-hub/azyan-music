package com.azyan.music.ui.library.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.DeleteOutline
import androidx.compose.material.icons.rounded.Favorite
import androidx.compose.material.icons.rounded.FavoriteBorder
import androidx.compose.material.icons.rounded.GraphicEq
import androidx.compose.material.icons.rounded.MoreVert
import androidx.compose.material.icons.rounded.PlayArrow
import androidx.compose.material.icons.rounded.PlaylistAdd
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.azyan.music.data.Song
import com.azyan.music.ui.util.formatDuration

@Composable
fun SongRow(
    song: Song,
    isCurrent: Boolean,
    isPlaying: Boolean,
    isFavorite: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    onToggleFavorite: (() -> Unit)? = null,
    onAddToPlaylist: (() -> Unit)? = null,
    onRemove: (() -> Unit)? = null
) {
    var menuOpen by remember { mutableStateOf(false) }
    val hasMenu = onToggleFavorite != null || onAddToPlaylist != null || onRemove != null

    Row(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(start = 16.dp, end = if (hasMenu) 4.dp else 16.dp, top = 8.dp, bottom = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        SongArtwork(song = song, modifier = Modifier.size(48.dp))

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = song.title,
                style = MaterialTheme.typography.bodyLarge,
                color = if (isCurrent) {
                    MaterialTheme.colorScheme.primary
                } else {
                    MaterialTheme.colorScheme.onSurface
                },
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = song.artist,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }

        if (isFavorite) {
            Icon(
                imageVector = Icons.Rounded.Favorite,
                contentDescription = "Favorit",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(16.dp)
            )
        }

        if (isCurrent && isPlaying) {
            Icon(
                imageVector = Icons.Rounded.GraphicEq,
                contentDescription = "Sedang diputar",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(20.dp)
            )
        }

        Text(
            text = formatDuration(song.durationMs),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        if (hasMenu) {
            Box {
                IconButton(onClick = { menuOpen = true }) {
                    Icon(
                        imageVector = Icons.Rounded.MoreVert,
                        contentDescription = "Opsi lain"
                    )
                }
                DropdownMenu(expanded = menuOpen, onDismissRequest = { menuOpen = false }) {
                    DropdownMenuItem(
                        text = { Text("Putar sekarang") },
                        leadingIcon = { Icon(Icons.Rounded.PlayArrow, contentDescription = null) },
                        onClick = {
                            menuOpen = false
                            onClick()
                        }
                    )
                    onToggleFavorite?.let { toggle ->
                        DropdownMenuItem(
                            text = {
                                Text(if (isFavorite) "Hapus dari favorit" else "Tambah ke favorit")
                            },
                            leadingIcon = {
                                Icon(
                                    imageVector = if (isFavorite) {
                                        Icons.Rounded.FavoriteBorder
                                    } else {
                                        Icons.Rounded.Favorite
                                    },
                                    contentDescription = null
                                )
                            },
                            onClick = {
                                menuOpen = false
                                toggle()
                            }
                        )
                    }
                    onAddToPlaylist?.let { add ->
                        DropdownMenuItem(
                            text = { Text("Tambah ke playlist") },
                            leadingIcon = {
                                Icon(Icons.Rounded.PlaylistAdd, contentDescription = null)
                            },
                            onClick = {
                                menuOpen = false
                                add()
                            }
                        )
                    }
                    onRemove?.let { remove ->
                        DropdownMenuItem(
                            text = { Text("Hapus dari playlist") },
                            leadingIcon = {
                                Icon(Icons.Rounded.DeleteOutline, contentDescription = null)
                            },
                            onClick = {
                                menuOpen = false
                                remove()
                            }
                        )
                    }
                }
            }
        }
    }
}
