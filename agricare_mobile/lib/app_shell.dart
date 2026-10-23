import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'features/advisory/screens/advisory_feed_screen.dart';
import 'features/auth/auth_controller.dart';
import 'features/farms/screens/farms_screen.dart';

/// Shown once the user is authenticated - the farms/advisory/profile loop a
/// logged-in farmer lives in day to day.
class AppShell extends ConsumerStatefulWidget {
  const AppShell({super.key});

  @override
  ConsumerState<AppShell> createState() => _AppShellState();
}

class _AppShellState extends ConsumerState<AppShell> {
  int _tabIndex = 0;

  static const _titles = ['Advisories', 'My Farms', 'Profile'];

  @override
  Widget build(BuildContext context) {
    final pages = [
      const AdvisoryFeedScreen(),
      const FarmsScreen(),
      const _ProfileTab(),
    ];

    return Scaffold(
      appBar: AppBar(title: Text(_titles[_tabIndex])),
      body: pages[_tabIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tabIndex,
        onDestinationSelected: (index) => setState(() => _tabIndex = index),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.warning_amber_rounded), label: 'Advisories'),
          NavigationDestination(icon: Icon(Icons.agriculture), label: 'Farms'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

class _ProfileTab extends ConsumerWidget {
  const _ProfileTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authControllerProvider).value;

    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          CircleAvatar(radius: 32, child: Text((user?.username ?? '?').substring(0, 1).toUpperCase())),
          const SizedBox(height: 12),
          Text(user?.username ?? '', style: Theme.of(context).textTheme.titleLarge),
          Text(user?.role ?? ''),
          if (user?.phoneNumber.isNotEmpty ?? false) Text(user!.phoneNumber),
          const SizedBox(height: 24),
          OutlinedButton(
            onPressed: () => ref.read(authControllerProvider.notifier).logout(),
            child: const Text('Log out'),
          ),
        ],
      ),
    );
  }
}
