import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Persists the auth token across app restarts. A thin wrapper around
/// secure storage so the rest of the app never touches the storage API
/// directly - if the persistence mechanism changes later, this is the only
/// file that needs to.
class TokenStorage {
  TokenStorage(this._storage);

  final FlutterSecureStorage _storage;
  static const _tokenKey = 'auth_token';

  Future<String?> read() => _storage.read(key: _tokenKey);

  Future<void> write(String token) => _storage.write(key: _tokenKey, value: token);

  Future<void> clear() => _storage.delete(key: _tokenKey);
}
