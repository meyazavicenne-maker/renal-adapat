package com.renal.adapat.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.renal.adapat.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CalculatorScreen() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Calculateurs médicaux") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Primary,
                    titleContentColor = Surface
                )
            )
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(
                    "Calculateurs disponibles",
                    style = MaterialTheme.typography.headlineSmall,
                    color = TextPrimary
                )
            }
            
            item {
                CalculatorCard(
                    title = "DFG - Cockcroft-Gault",
                    description = "Débit de filtration glomérulaire",
                    icon = Icons.Default.Science,
                    color = Primary
                )
            }
            
            item {
                CalculatorCard(
                    title = "DFG - MDRD",
                    description = "Modification of Diet in Renal Disease",
                    icon = Icons.Default.Biotech,
                    color = Secondary
                )
            }
            
            item {
                CalculatorCard(
                    title = "DFG - CKD-EPI",
                    description = "Chronic Kidney Disease Epidemiology",
                    icon = Icons.Default.Analytics,
                    color = PrimaryLight
                )
            }
            
            item {
                CalculatorCard(
                    title = "Sodium corrigé",
                    description = "Correction selon la glycémie",
                    icon = Icons.Default.WaterDrop,
                    color = Primary
                )
            }
            
            item {
                CalculatorCard(
                    title = "Déficit hydrique",
                    description = "Calcul du déficit en eau",
                    icon = Icons.Default.Opacity,
                    color = Secondary
                )
            }
            
            item {
                CalculatorCard(
                    title = "Trou anionique",
                    description = "Anion gap",
                    icon = Icons.Default.ElectricBolt,
                    color = PrimaryLight
                )
            }
            
            item {
                Text(
                    "Calculateurs interactifs complets à venir",
                    style = MaterialTheme.typography.bodyMedium,
                    color = TextSecondary,
                    modifier = Modifier.padding(top = 16.dp)
                )
            }
        }
    }
}

@Composable
fun CalculatorCard(
    title: String,
    description: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    color: androidx.compose.ui.graphics.Color
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = color,
                modifier = Modifier.size(40.dp)
            )
            
            Spacer(modifier = Modifier.width(16.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    color = TextPrimary
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = TextSecondary
                )
            }
        }
    }
}
