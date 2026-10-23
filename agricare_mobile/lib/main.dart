import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app_shell.dart';
import 'features/auth/auth_controller.dart';
import 'features/auth/screens/login_screen.dart';

void main() {
  runApp(const ProviderScope(child: AgriCareApp()));
}

class AgriCareApp extends StatelessWidget {
  const AgriCareApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AgriCare',
      theme: ThemeData(colorSchemeSeed: const Color(0xFF2E7D32), useMaterial3: true),
      home: const _AuthGate(),
    );
  }
}

/// Root-level switch between logged-out and logged-in UI, driven entirely
/// by authControllerProvider's state - AuthController.build() checks for a
/// stored token on startup, so this also covers the "already logged in from
/// a previous session" case without any extra wiring here.
class _AuthGate extends ConsumerWidget {
  const _AuthGate();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authControllerProvider);

    return authState.when(
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (error, _) => Scaffold(
        body: Center(child: Text('Something went wrong.\n$error', textAlign: TextAlign.center)),
      ),
      data: (user) => user == null ? const LoginScreen() : const AppShell(),
    );
  }
}
