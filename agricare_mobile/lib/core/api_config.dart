/// Base URL for the AgriCare Django backend.
///
/// - Chrome/web (same machine as the dev server): 127.0.0.1 works directly.
/// - Android emulator: use 10.0.2.2 instead of 127.0.0.1 (the emulator's
///   alias for the host machine's localhost).
/// - A real device: use the host machine's LAN IP.
///
/// Override at build/run time with:
///   flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://127.0.0.1:8000/api/v1',
);
