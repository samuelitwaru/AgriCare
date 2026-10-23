import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers.dart';
import 'models/zone.dart';

class ZonesRepository {
  ZonesRepository(this._dio);

  final Dio _dio;

  /// Zones are a small, mostly-static reference list (135 districts), so a
  /// single unpaginated-feeling call is fine here - page_size is bumped past
  /// the DRF default (25) to fetch them all in one request for the dropdown.
  Future<List<Zone>> list() async {
    final response = await _dio.get('/zones/', queryParameters: {'page_size': 200});
    final results = (response.data as Map<String, dynamic>)['results'] as List;
    return results.map((e) => Zone.fromJson(e as Map<String, dynamic>)).toList();
  }
}

final zonesRepositoryProvider = Provider<ZonesRepository>((ref) {
  return ZonesRepository(ref.watch(dioProvider));
});

final zonesListProvider = FutureProvider<List<Zone>>((ref) {
  return ref.watch(zonesRepositoryProvider).list();
});
