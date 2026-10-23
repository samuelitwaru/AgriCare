class Zone {
  const Zone({required this.code, required this.name, required this.region});

  factory Zone.fromJson(Map<String, dynamic> json) => Zone(
        code: json['code'] as String,
        name: json['name'] as String,
        region: json['region'] as String? ?? '',
      );

  final String code;
  final String name;
  final String region;
}
