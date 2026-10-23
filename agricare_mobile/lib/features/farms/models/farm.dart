class Farm {
  const Farm({
    required this.id,
    required this.name,
    required this.cropType,
    required this.sizeAcres,
    required this.zone,
    required this.zoneName,
  });

  factory Farm.fromJson(Map<String, dynamic> json) => Farm(
        id: json['id'] as int,
        name: json['name'] as String,
        cropType: json['crop_type'] as String,
        sizeAcres: json['size_acres'] == null ? null : double.tryParse(json['size_acres'].toString()),
        zone: json['zone'] as String?,
        zoneName: json['zone_name'] as String?,
      );

  final int id;
  final String name;
  final String cropType;
  final double? sizeAcres;
  final String? zone; // the zone's `code`, e.g. "UG3064" - not its numeric id
  final String? zoneName;
}
