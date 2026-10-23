class Advisory {
  const Advisory({
    required this.id,
    required this.farmId,
    required this.advisoryType,
    required this.title,
    required this.message,
    required this.riskLevel,
    required this.source,
    required this.generatedAt,
  });

  factory Advisory.fromJson(Map<String, dynamic> json) => Advisory(
        id: json['id'] as int,
        farmId: json['farm'] as int,
        advisoryType: json['advisory_type'] as String,
        title: json['title'] as String,
        message: json['message'] as String,
        riskLevel: json['risk_level'] as String,
        source: json['source'] as String,
        generatedAt: DateTime.parse(json['generated_at'] as String),
      );

  final int id;
  final int farmId;
  final String advisoryType;
  final String title;
  final String message;
  final String riskLevel; // low | medium | high
  final String source; // rule_based | ml_model | gen_ai
  final DateTime generatedAt;
}
