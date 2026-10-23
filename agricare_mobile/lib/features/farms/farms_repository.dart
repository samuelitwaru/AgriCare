import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers.dart';
import 'models/farm.dart';

class FarmsRepository {
  FarmsRepository(this._dio);

  final Dio _dio;

  Future<List<Farm>> list() async {
    final response = await _dio.get('/farms/');
    final results = (response.data as Map<String, dynamic>)['results'] as List;
    return results.map((e) => Farm.fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<Farm> create({required String name, required String cropType, String? zoneCode, double? sizeAcres}) async {
    final response = await _dio.post('/farms/', data: {
      'name': name,
      'crop_type': cropType,
      if (zoneCode != null) 'zone': zoneCode,
      if (sizeAcres != null) 'size_acres': sizeAcres,
    });
    return Farm.fromJson(response.data as Map<String, dynamic>);
  }
}

final farmsRepositoryProvider = Provider<FarmsRepository>((ref) {
  return FarmsRepository(ref.watch(dioProvider));
});

/// autoDispose + family-less list provider: refresh by calling
/// ref.invalidate(farmsListProvider) after a successful create, rather than
/// maintaining separate mutable list state by hand.
final farmsListProvider = FutureProvider<List<Farm>>((ref) {
  return ref.watch(farmsRepositoryProvider).list();
});
