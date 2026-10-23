import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers.dart';
import 'models/advisory.dart';

class AdvisoryRepository {
  AdvisoryRepository(this._dio);

  final Dio _dio;

  /// Read-only by design on the backend - advisories are generated
  /// server-side by the rule-based/ML/Gen-AI pipeline, never submitted by
  /// the app. The API already scopes this to the caller's own farms.
  Future<List<Advisory>> list() async {
    final response = await _dio.get('/advisories/');
    final results = (response.data as Map<String, dynamic>)['results'] as List;
    return results.map((e) => Advisory.fromJson(e as Map<String, dynamic>)).toList();
  }
}

final advisoryRepositoryProvider = Provider<AdvisoryRepository>((ref) {
  return AdvisoryRepository(ref.watch(dioProvider));
});

final advisoryListProvider = FutureProvider<List<Advisory>>((ref) {
  return ref.watch(advisoryRepositoryProvider).list();
});
