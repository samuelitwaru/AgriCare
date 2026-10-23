import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers.dart';
import 'models/user.dart';

class AuthRepository {
  AuthRepository(this._dio);

  final Dio _dio;

  /// Returns (user, token). Matches the backend's register response shape:
  /// {"user": {...}, "token": "..."} - see apps/accounts/views.py RegisterView.
  Future<(User, String)> register({
    required String username,
    required String password,
    String? phoneNumber,
  }) async {
    final response = await _dio.post('/auth/register/', data: {
      'username': username,
      'password': password,
      if (phoneNumber != null && phoneNumber.isNotEmpty) 'phone_number': phoneNumber,
    });
    final data = response.data as Map<String, dynamic>;
    return (User.fromJson(data['user'] as Map<String, dynamic>), data['token'] as String);
  }

  Future<String> login({required String username, required String password}) async {
    final response = await _dio.post('/auth/login/', data: {
      'username': username,
      'password': password,
    });
    return (response.data as Map<String, dynamic>)['token'] as String;
  }

  Future<User> me() async {
    final response = await _dio.get('/users/me/');
    return User.fromJson(response.data as Map<String, dynamic>);
  }
}

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(ref.watch(dioProvider));
});
