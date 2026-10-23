// Basic smoke test: the app should land on the login screen when there's no
// stored auth token. TokenStorage is overridden with a fake rather than the
// real flutter_secure_storage, which needs a platform channel unavailable
// in plain widget tests.

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:agricare_mobile/core/token_storage.dart';
import 'package:agricare_mobile/core/providers.dart';
import 'package:agricare_mobile/main.dart';

class _FakeTokenStorage implements TokenStorage {
  String? _token;

  @override
  Future<void> clear() async => _token = null;

  @override
  Future<String?> read() async => _token;

  @override
  Future<void> write(String token) async => _token = token;
}

void main() {
  testWidgets('shows the login screen when logged out', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [tokenStorageProvider.overrideWithValue(_FakeTokenStorage())],
        child: const AgriCareApp(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Agri-Climate Advisory'), findsOneWidget);
    expect(find.text('Log in'), findsOneWidget);
  });
}
