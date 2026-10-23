class User {
  const User({
    required this.id,
    required this.username,
    required this.email,
    required this.role,
    required this.phoneNumber,
    required this.preferredLanguage,
    required this.organization,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['id'] as int,
        username: json['username'] as String,
        email: json['email'] as String? ?? '',
        role: json['role'] as String,
        phoneNumber: json['phone_number'] as String? ?? '',
        preferredLanguage: json['preferred_language'] as String? ?? 'en',
        organization: json['organization'] as String? ?? '',
      );

  final int id;
  final String username;
  final String email;
  final String role;
  final String phoneNumber;
  final String preferredLanguage;
  final String organization;
}
