package com.azyan.music

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import com.azyan.music.ui.WelcomeScreen
import com.azyan.music.ui.theme.AzyanMusicTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent {
            AzyanMusicApp()
        }
    }
}

@Composable
fun AzyanMusicApp() {
    AzyanMusicTheme {
        WelcomeScreen()
    }
}

@Preview(showBackground = true)
@Composable
private fun WelcomePreview() {
    AzyanMusicTheme(dynamicColor = false) {
        WelcomeScreen()
    }
}
