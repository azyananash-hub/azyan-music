package com.azyan.music.ui.library

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material.icons.rounded.ChevronRight
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Folder
import androidx.compose.material.icons.rounded.MusicOff
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.azyan.music.data.Song
import com.azyan.music.playback.PlayerManager
import com.azyan.music.playback.PlayerUiState
import com.azyan.music.ui.library.components.MiniPlayer
import com.azyan.music.ui.library.components.NowPlayingSheet
import com.azyan.music.ui.library.components.PermissionScreen
import com.azyan.music.ui.library.components.SongRow
import com.azyan.music.ui.util.PermissionUtils

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MusicHomeScreen(viewModel: LibraryViewModel = viewModel()) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current

    val hasPermission by viewModel.hasPermission.collectAsStateWithLifecycle()
    val songs by viewModel.songs.collectAsStateWithLifecycle()
    val query by viewModel.query.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()
    val playerState by PlayerManager.state.collectAsStateWithLifecycle()

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted -> viewModel.onPermissionResult(granted) }

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) viewModel.refreshPermission()
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    if (!hasPermission) {
        PermissionScreen(onRequest = { permissionLauncher.launch(PermissionUtils.audioPermission()) })
        return
    }

    var selectedTab by rememberSaveable { mutableIntStateOf(0) }
    var isSearching by rememberSaveable { mutableStateOf(false) }
    var openFolder by rememberSaveable { mutableStateOf<String?>(null) }
    var showNowPlaying by rememberSaveable { mutableStateOf(false) }

    val filteredSongs = remember(songs, query) {
        val q = query.trim()
        if (q.isBlank()) {
            songs
        } else {
            songs.filter { song ->
                song.title.contains(q, ignoreCase = true) ||
                    song.artist.contains(q, ignoreCase = true) ||
                    song.album.contains(q, ignoreCase = true)
            }
        }
    }

    val folders = remember(songs) {
        songs.groupBy { it.folder }
            .toList()
            .sortedBy { (name, _) -> name.lowercase() }
    }

    val folderSongs = remember(songs, openFolder) {
        openFolder?.let { folder -> songs.filter { it.folder == folder } } ?: emptyList()
    }

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = {
                        Column {
                            Text(
                                text = openFolder ?: "Azyan Music",
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (openFolder == null && !isSearching) {
                                Text(
                                    text = "${songs.size} lagu",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    },
                    navigationIcon = {
                        if (openFolder != null) {
                            IconButton(onClick = { openFolder = null }) {
                                Icon(Icons.Rounded.ArrowBack, contentDescription = "Kembali")
                            }
                        }
                    },
                    actions = {
                        if (isSearching) {
                            IconButton(onClick = {
                                isSearching = false
                                viewModel.setQuery("")
                            }) {
                                Icon(Icons.Rounded.Close, contentDescription = "Tutup pencarian")
                            }
                        } else {
                            IconButton(onClick = { isSearching = true }) {
                                Icon(Icons.Rounded.Search, contentDescription = "Cari")
                            }
                        }
                    }
                )

                if (isSearching) {
                    OutlinedTextField(
                        value = query,
                        onValueChange = viewModel::setQuery,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        placeholder = { Text("Cari judul, artis, atau album") },
                        leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = null) },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp)
                    )
                } else if (openFolder == null) {
                    TabRow(selectedTabIndex = selectedTab) {
                        Tab(
                            selected = selectedTab == 0,
                            onClick = { selectedTab = 0 },
                            text = { Text("Lagu") }
                        )
                        Tab(
                            selected = selectedTab == 1,
                            onClick = { selectedTab = 1 },
                            text = { Text("Folder") }
                        )
                    }
                }
            }
        },
        bottomBar = {
            if (playerState.currentSong != null) {
                MiniPlayer(state = playerState, onOpen = { showNowPlaying = true })
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when {
                isLoading -> CircularProgressIndicator(Modifier.align(Alignment.Center))

                query.isNotBlank() -> SongList(
                    songs = filteredSongs,
                    playerState = playerState,
                    emptyText = "Tidak ada lagu yang cocok",
                    onPlay = { index -> PlayerManager.play(context, filteredSongs, index) }
                )

                openFolder != null -> SongList(
                    songs = folderSongs,
                    playerState = playerState,
                    emptyText = "Folder ini kosong",
                    onPlay = { index -> PlayerManager.play(context, folderSongs, index) }
                )

                selectedTab == 0 -> SongList(
                    songs = songs,
                    playerState = playerState,
                    emptyText = "Belum ada lagu di HP ini",
                    onPlay = { index -> PlayerManager.play(context, songs, index) }
                )

                else -> FolderList(folders = folders, onOpen = { openFolder = it })
            }
        }
    }

    if (showNowPlaying && playerState.currentSong != null) {
        NowPlayingSheet(state = playerState, onDismiss = { showNowPlaying = false })
    }
}

@Composable
private fun SongList(
    songs: List<Song>,
    playerState: PlayerUiState,
    onPlay: (Int) -> Unit,
    emptyText: String
) {
    if (songs.isEmpty()) {
        EmptyState(text = emptyText)
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(top = 8.dp, bottom = 24.dp)
    ) {
        itemsIndexed(items = songs, key = { _, song -> song.id }) { index, song ->
            SongRow(
                song = song,
                isCurrent = playerState.currentSong?.id == song.id,
                isPlaying = playerState.isPlaying,
                onClick = { onPlay(index) }
            )
        }
    }
}

@Composable
private fun FolderList(
    folders: List<Pair<String, List<Song>>>,
    onOpen: (String) -> Unit
) {
    if (folders.isEmpty()) {
        EmptyState(text = "Belum ada folder musik")
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        items(items = folders, key = { (name, _) -> name }) { (name, folderSongs) ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onOpen(name) }
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Rounded.Folder,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = name,
                        style = MaterialTheme.typography.bodyLarge,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "${folderSongs.size} lagu",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Icon(
                    imageVector = Icons.Rounded.ChevronRight,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun EmptyState(text: String) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Rounded.MusicOff,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(48.dp)
        )
        Spacer(Modifier.height(12.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
    }
}
