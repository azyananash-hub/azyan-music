package com.azyan.music.ui.theme

import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.ui.graphics.Color

// Seed palette: cool "ocean" accent that reads well on both themes.
val AccentBlue = Color(0xFF7FD1FF)
val AccentBlueDeep = Color(0xFF00547A)
val AccentTeal = Color(0xFF4DD6C1)
val Ink = Color(0xFF101418)

val LightColors = lightColorScheme(
    primary = AccentBlueDeep,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFC7E7FF),
    onPrimaryContainer = Color(0xFF001E2D),
    secondary = Color(0xFF00696B),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFCCE8E7),
    onSecondaryContainer = Color(0xFF002020),
    tertiary = Color(0xFF4B607C),
    background = Color(0xFFFBFCFE),
    onBackground = Color(0xFF191C1E),
    surface = Color(0xFFFBFCFE),
    onSurface = Color(0xFF191C1E),
    surfaceVariant = Color(0xFFDCE3EA),
    onSurfaceVariant = Color(0xFF40484D)
)

val DarkColors = darkColorScheme(
    primary = AccentBlue,
    onPrimary = Color(0xFF00344A),
    primaryContainer = Color(0xFF004C6B),
    onPrimaryContainer = Color(0xFFC7E7FF),
    secondary = Color(0xFF7FD4D3),
    onSecondary = Color(0xFF003737),
    secondaryContainer = Color(0xFF004F50),
    onSecondaryContainer = Color(0xFFCCE8E7),
    tertiary = Color(0xFFB3C8E8),
    background = Ink,
    onBackground = Color(0xFFE1E3E5),
    surface = Ink,
    onSurface = Color(0xFFE1E3E5),
    surfaceVariant = Color(0xFF40484D),
    onSurfaceVariant = Color(0xFFC0C7CD)
)
