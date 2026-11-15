package com.azyan.music.ui.library

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.azyan.music.data.MediaStoreScanner
import com.azyan.music.data.Song
import com.azyan.music.ui.util.PermissionUtils
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LibraryViewModel(application: Application) : AndroidViewModel(application) {

    private val _songs = MutableStateFlow<List<Song>>(emptyList())
    val songs = _songs.asStateFlow()

    private val _query = MutableStateFlow("")
    val query = _query.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private val _hasPermission = MutableStateFlow(PermissionUtils.hasAudioPermission(application))
    val hasPermission = _hasPermission.asStateFlow()

    private var refreshJob: Job? = null

    init {
        if (_hasPermission.value) refresh()
    }

    fun refreshPermission() {
        val granted = PermissionUtils.hasAudioPermission(getApplication<Application>())
        val wasGranted = _hasPermission.value
        _hasPermission.value = granted
        if (granted && (!wasGranted || _songs.value.isEmpty())) refresh()
    }

    fun onPermissionResult(granted: Boolean) {
        _hasPermission.value = granted
        if (granted) refresh()
    }

    fun refresh() {
        if (!_hasPermission.value) return
        refreshJob?.cancel()
        refreshJob = viewModelScope.launch {
            _isLoading.value = true
            _songs.value = withContext(Dispatchers.IO) {
                MediaStoreScanner.scan(getApplication<Application>())
            }
            _isLoading.value = false
        }
    }

    fun setQuery(value: String) {
        _query.value = value
    }
}
