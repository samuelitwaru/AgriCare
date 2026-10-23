import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../farms_repository.dart';
import 'add_farm_screen.dart';

class FarmsScreen extends ConsumerWidget {
  const FarmsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final farmsAsync = ref.watch(farmsListProvider);

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () async => ref.invalidate(farmsListProvider),
        child: farmsAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => ListView(
            children: [
              const SizedBox(height: 120),
              Center(child: Text('Could not load farms.\n$error', textAlign: TextAlign.center)),
            ],
          ),
          data: (farms) {
            if (farms.isEmpty) {
              return ListView(
                children: const [
                  SizedBox(height: 120),
                  Center(child: Text('No farms registered yet. Tap + to add one.')),
                ],
              );
            }
            return ListView.separated(
              padding: const EdgeInsets.all(12),
              itemCount: farms.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final farm = farms[index];
                return Card(
                  child: ListTile(
                    title: Text(farm.name),
                    subtitle: Text(
                      '${farm.cropType} · ${farm.zoneName ?? "No zone set"}'
                      '${farm.sizeAcres != null ? " · ${farm.sizeAcres} acres" : ""}',
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final created = await Navigator.of(context).push<bool>(
            MaterialPageRoute(builder: (_) => const AddFarmScreen()),
          );
          if (created == true) {
            ref.invalidate(farmsListProvider);
          }
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
