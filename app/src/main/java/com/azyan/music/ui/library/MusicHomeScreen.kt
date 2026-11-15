package com.azyan.music.ui.library

import android.Manifest
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material.icons.rounded.ChevronRight
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.DeleteOutline
import androidx.compose.material.icons.rounded.Folder
import androidx.compose.material.icons.rounded.MusicOff
import androidx.compose.material.icons.rounded.Notifications
import androidx.compose.material.icons.rounded.PlayArrow
import androidx.compose.material.icons.rounded.QueueMusic
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
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
import com.azyan.music.data.LibraryStore
import com.azyan.music.data.Playlist
import com.azyan.music.data.Song
import com.azyan.music.data.toSong
import com.azyan.music.playback.PlayerController
import com.azyan.music.playback.PlayerUiState
import com.azyan.music.ui.library.components.AddToPlaylistDialog
import com.azyan.music.ui.library.components.CreatePlaylistDialog
import com.azyan.music.ui.library.components.DeletePlaylistDialog
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
    val playerState by PlayerController.state.collectAsStateWithLifecycle()

    var notificationGranted by remember {
        mutableStateOf(PermissionUtils.hasNotificationPermission(context))
    }
    var askedNotification by rememberSaveable { mutableStateOf(false) }

    val notificationLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted -> notificationGranted = granted }

    fun requestNotificationPermissionIfNeeded() {
        if (notificationGranted || askedNotification) return
        askedNotification = true
        notificationLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted -> viewModel.onPermissionResult(granted) }

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                viewModel.refreshPermission()
                notificationGranted = PermissionUtils.hasNotificationPermission(context)
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    LaunchedEffect(Unit) {
        PlayerController.connect(context)
    }

    if (!hasPermission) {
        PermissionScreen(onRequest = { permissionLauncher.launch(PermissionUtils.audioPermission()) })
        return
    }

    var selectedTab by rememberSaveable { mutableIntStateOf(0) }
    var isSearching by rememberSaveable { mutableStateOf(false) }
    var openFolder by rememberSaveable { mutableStateOf<String?>(null) }
    var openPlaylistId by rememberSaveable { mutableStateOf<String?>(null) }
    var showNowPlaying by rememberSaveable { mutableStateOf(false) }
    var showCreatePlaylist by remember { mutableStateOf(false) }
    var playlistTarget by remember { mutableStateOf<List<Song>?>(null) }
    var playlistToDelete by remember { mutableStateOf<Playlist?>(null) }

    val store by LibraryStore.data.collectAsStateWithLifecycle()
    val favoriteIds = remember(store.favorites) { store.favorites.map { it.id }.toSet() }
    val favoriteSongs = remember(store.favorites) { store.favorites.map { it.toSong() } }
    val selectedPlaylist = remember(store.playlists, openPlaylistId) {
        store.playlists.firstOrNull { it.id == openPlaylistId }
    }
    val playlistSongs = remember(selectedPlaylist) {
        selectedPlaylist?.songs?.map { it.toSong() } ?: emptyList()
    }

    LaunchedEffect(openPlaylistId, store.playlists) {
        if (openPlaylistId != null && store.playlists.none { it.id == openPlaylistId }) {
            openPlaylistId = null
        }
    }

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

    val isDetail = openFolder != null || selectedPlaylist != null

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = {
                        Column {
                            Text(
                                text = openFolder ?: selectedPlaylist?.name ?: "Azyan Music",
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            if (!isDetail && !isSearching) {
                                Text(
                                    text = "${songs.size} lagu",
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    },
                    navigationIcon = {
                        if (isDetail || openFolder != null) {
                            IconButton(onClick = {
                                openFolder = null
                                openPlaylistId = null
                            }) {
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
                } else if (!isDetail) {
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
                        Tab(
                            selected = selectedTab == 2,
                            onClick = { selectedTab = 2 },
                            text = { Text("Playlist") }
                        )
                        Tab(
                            selected = selectedTab == 3,
                            onClick = { selectedTab = 3 },
                            text = { Text("Favorit") }
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
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            if (!notificationGranted) {
                NotificationBanner(
                    onAllow = { requestNotificationPermissionIfNeeded() },
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                )
            }

            Box(modifier = Modifier.weight(1f)) {
                when {
                    isLoading -> CircularProgressIndicator(Modifier.align(Alignment.Center))

                    query.isNotBlank() -> SongList(
                        songs = filteredSongs,
                        playerState = playerState,
                        favoriteIds = favoriteIds,
                        emptyText = "Tidak ada lagu yang cocok",
                        onPlay = { index ->
                            requestNotificationPermissionIfNeeded()
                            PlayerController.play(context, filteredSongs, index)
                        },
                        onToggleFavorite = { LibraryStore.toggleFavorite(it) },
                        onAddToPlaylist = { playlistTarget = listOf(it) }
                    )

                    openFolder != null -> SongList(
                        songs = folderSongs,
                        playerState = playerState,
                        favoriteIds = favoriteIds,
                        emptyText = "Folder ini kosong",
                        onPlay = { index ->
                            requestNotificationPermissionIfNeeded()
                            PlayerController.play(context, folderSongs, index)
                        },
                        onToggleFavorite = { LibraryStore.toggleFavorite(it) },
                        onAddToPlaylist = { playlistTarget = listOf(it) }
                    )

                    selectedPlaylist != null -> Column(modifier = Modifier.fillMaxSize()) {
                        PlaylistHeader(
                            songCount = playlistSongs.size,
                            onPlayAll = {
                                if (playlistSongs.isNotEmpty()) {
                                    requestNotificationPermissionIfNeeded()
                                    PlayerController.play(context, playlistSongs, 0)
                                }
                            }
                        )
                        SongList(
                            songs = playlistSongs,
                            playerState = playerState,
                            favoriteIds = favoriteIds,
                            emptyText = "Playlist ini masih kosong",
                            onPlay = { index ->
                                requestNotificationPermissionIfNeeded()
                                PlayerController.play(context, playlistSongs, index)
                            },
                            onToggleFavorite = { LibraryStore.toggleFavorite(it) },
                            onAddToPlaylist = null,
                            onRemove = { song ->
                                LibraryStore.removeSongFromPlaylist(selectedPlaylist.id, song.id)
                            }
                        )
                    }

                    selectedTab == 0 -> SongList(
                        songs = songs,
                        playerState = playerState,
                        favoriteIds = favoriteIds,
                        emptyText = "Belum ada lagu di HP ini",
                        onPlay = { index ->
                            requestNotificationPermissionIfNeeded()
                            PlayerController.play(context, songs, index)
                        },
                        onToggleFavorite = { LibraryStore.toggleFavorite(it) },
                        onAddToPlaylist = { playlistTarget = listOf(it) }
                    )

                    selectedTab == 1 -> FolderList(folders = folders, onOpen = { openFolder = it })

                    selectedTab == 2 -> PlaylistList(
                        playlists = store.playlists,
                        onCreate = { showCreatePlaylist = true },
                        onOpen = { openPlaylistId = it },
                        onDelete = { playlistToDelete = it }
                    )

                    else -> SongList(
                        songs = favoriteSongs,
                        playerState = playerState,
                        favoriteIds = favoriteIds,
                        emptyText = "Belum ada lagu favorit.\nTekan menu ⋮ pada lagu lalu pilih \"Tambah ke favorit\".",
                        onPlay = { index ->
                            requestNotificationPermissionIfNeeded()
                            PlayerController.play(context, favoriteSongs, index)
                        },
                        onToggleFavorite = { LibraryStore.toggleFavorite(it) },
                        onAddToPlaylist = { playlistTarget = listOf(it) }
                    )
                }
            }
        }
    }

    playerState.currentSong?.let { current ->
        if (showNowPlaying) {
            NowPlayingSheet(
                state = playerState,
                isFavorite = current.id in favoriteIds,
                onToggleFavorite = { LibraryStore.toggleFavorite(current) },
                onDismiss = { showNowPlaying = false }
            )
        }
    }

    if (showCreatePlaylist) {
        CreatePlaylistDialog(
            onDismiss = { showCreatePlaylist = false },
            onCreate = { name ->
                val id = LibraryStore.createPlaylist(name)
                showCreatePlaylist = false
                selectedTab = 2
                openPlaylistId = id
            }
        )
    }

    playlistTarget?.let { target ->
        AddToPlaylistDialog(
            playlists = store.playlists,
            onDismiss = { playlistTarget = null },
            onPick = { playlistId ->
                LibraryStore.addSongsToPlaylist(playlistId, target)
                playlistTarget = null
            },
            onCreateAndAdd = { name ->
                val id = LibraryStore.createPlaylist(name)
                LibraryStore.addSongsToPlaylist(id, target)
                playlistTarget = null
            }
        )
    }

    playlistToDelete?.let { playlist ->
        DeletePlaylistDialog(
            playlistName = playlist.name,
            onDismiss = { playlistToDelete = null },
            onConfirm = {
                LibraryStore.deletePlaylist(playlist.id)
                playlistToDelete = null
            }
        )
    }
}

@Composable
private fun PlaylistHeader(songCount: Int, onPlayAll: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Button(onClick = onPlayAll, enabled = songCount > 0) {
            Icon(Icons.Rounded.PlayArrow, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text("Putar semua")
        }
        Text(
            text = "$songCount lagu",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun PlaylistList(
    playlists: List<Playlist>,
    onCreate: () -> Unit,
    onOpen: (String) -> Unit,
    onDelete: (Playlist) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(onClick = onCreate)
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Rounded.Add,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = "Buat playlist baru",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }

        if (playlists.isEmpty()) {
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        imageVector = Icons.Rounded.QueueMusic,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(48.dp)
                    )
                    Spacer(Modifier.height(12.dp))
                    Text(
                        text = "Belum ada playlist",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center
                    )
                }
            }
        }

        items(items = playlists, key = { it.id }) { playlist ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onOpen(playlist.id) }
                    .padding(start = 16.dp, end = 4.dp, top = 8.dp, bottom = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Rounded.QueueMusic,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = playlist.name,
                        style = MaterialTheme.typography.bodyLarge,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "${playlist.songs.size} lagu",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                IconButton(onClick = { onDelete(playlist) }) {
                    Icon(
                        imageVector = Icons.Rounded.DeleteOutline,
                        contentDescription = "Hapus playlist",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun NotificationBanner(onAllow: () -> Unit, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.secondaryContainer
    ) {
        Row(
            modifier = Modifier.padding(start = 16.dp, end = 8.dp, top = 6.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(
                imageVector = Icons.Rounded.Notifications,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSecondaryContainer
            )
            Text(
                text = "Aktifkan notifikasi agar kontrol musik muncul di notifikasi & layar kunci.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSecondaryContainer,
                modifier = Modifier.weight(1f)
            )
            TextButton(onClick = onAllow) {
                Text("Izinkan")
            }
        }
    }
}

@Composable
private fun SongList(
    songs: List<Song>,
    playerState: PlayerUiState,
    favoriteIds: Set<Long>,
    onPlay: (Int) -> Unit,
    onToggleFavorite: (Song) -> Unit,
    emptyText: String,
    onAddToPlaylist: ((Song) -> Unit)? = null,
    onRemove: ((Song) -> Unit)? = null
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
                isFavorite = song.id in favoriteIds,
                onClick = { onPlay(index) },
                onToggleFavorite = { onToggleFavorite(song) },
                onAddToPlaylist = onAddToPlaylist?.let { add -> { add(song) } },
                onRemove = onRemove?.let { remove -> { remove(song) } }
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
