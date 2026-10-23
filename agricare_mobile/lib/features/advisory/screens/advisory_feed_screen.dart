import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../advisory_repository.dart';
import '../models/advisory.dart';

class AdvisoryFeedScreen extends ConsumerWidget {
  const AdvisoryFeedScreen({super.key});

  Color _riskColor(BuildContext context, String riskLevel) {
    switch (riskLevel) {
      case 'high':
        return Colors.red.shade700;
      case 'medium':
        return Colors.orange.shade700;
      default:
        return Colors.green.shade700;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final advisoriesAsync = ref.watch(advisoryListProvider);

    return RefreshIndicator(
      onRefresh: () async => ref.invalidate(advisoryListProvider),
      child: advisoriesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => ListView(
          children: [
            const SizedBox(height: 120),
            Center(child: Text('Could not load advisories.\n$error', textAlign: TextAlign.center)),
          ],
        ),
        data: (advisories) {
          if (advisories.isEmpty) {
            return ListView(
              children: const [
                SizedBox(height: 120),
                Center(
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 32),
                    child: Text(
                      'No advisories yet. Once your farm is registered to a zone, '
                      'climate and crop risk alerts will appear here.',
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ],
            );
          }
          return ListView.separated(
            padding: const EdgeInsets.all(12),
            itemCount: advisories.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (context, index) => _AdvisoryCard(
              advisory: advisories[index],
              riskColor: _riskColor(context, advisories[index].riskLevel),
            ),
          );
        },
      ),
    );
  }
}

class _AdvisoryCard extends StatelessWidget {
  const _AdvisoryCard({required this.advisory, required this.riskColor});

  final Advisory advisory;
  final Color riskColor;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 10,
                  height: 10,
                  decoration: BoxDecoration(color: riskColor, shape: BoxShape.circle),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    advisory.title,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(advisory.message),
            const SizedBox(height: 8),
            Text(
              '${advisory.riskLevel.toUpperCase()} risk · ${advisory.generatedAt.toLocal().toString().split('.').first}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
