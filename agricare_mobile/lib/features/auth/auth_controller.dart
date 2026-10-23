import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers.dart';
import 'auth_repository.dart';
import 'models/user.dart';

/// Session state: null user = logged out, non-null = logged in. Wrapped in
/// AsyncValue by AsyncNotifier so the UI can distinguish "still checking
/// stored token on startup" (loading) from "confirmed logged out" (data:
/// null) rather than treating both the same way.
class AuthController extends AsyncNotifier<User?> {
  @override
  Future<User?> build() async {
    final token = await ref.watch(tokenStorageProvider).read();
    if (token == null) return null;

    try {
      return await ref.watch(authRepositoryProvider).me();
    } on Object {
      // Stored token is stale/invalid (e.g. revoked server-side) - treat as
      // logged out rather than surfacing an error on every app launch.
      await ref.watch(tokenStorageProvider).clear();
      return null;
    }
  }

  Future<void> login({required String username, required String password}) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final token = await ref.read(authRepositoryProvider).login(username: username, password: password);
      await ref.read(tokenStorageProvider).write(token);
      return ref.read(authRepositoryProvider).me();
    });
  }

  Future<void> register({required String username, required String password, String? phoneNumber}) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final (user, token) = await ref.read(authRepositoryProvider).register(
            username: username,
            password: password,
            phoneNumber: phoneNumber,
          );
      await ref.read(tokenStorageProvider).write(token);
      return user;
    });
  }

  Future<void> logout() async {
    await ref.read(tokenStorageProvider).clear();
    state = const AsyncData(null);
  }
}

final authControllerProvider = AsyncNotifierProvider<AuthController, User?>(AuthController.new);
