import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../zones/zones_repository.dart';
import '../farms_repository.dart';

class AddFarmScreen extends ConsumerStatefulWidget {
  const AddFarmScreen({super.key});

  @override
  ConsumerState<AddFarmScreen> createState() => _AddFarmScreenState();
}

class _AddFarmScreenState extends ConsumerState<AddFarmScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _cropController = TextEditingController();
  final _sizeController = TextEditingController();
  String? _selectedZoneCode;
  bool _submitting = false;
  String? _error;

  @override
  void dispose() {
    _nameController.dispose();
    _cropController.dispose();
    _sizeController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _submitting = true;
      _error = null;
    });
    try {
      await ref.read(farmsRepositoryProvider).create(
            name: _nameController.text.trim(),
            cropType: _cropController.text.trim(),
            zoneCode: _selectedZoneCode,
            sizeAcres: _sizeController.text.isEmpty ? null : double.tryParse(_sizeController.text),
          );
      if (mounted) Navigator.of(context).pop(true);
    } catch (e) {
      setState(() => _error = 'Could not save farm. $e');
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final zonesAsync = ref.watch(zonesListProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Register Farm')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              if (_error != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
                ),
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(labelText: 'Farm name'),
                validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _cropController,
                decoration: const InputDecoration(labelText: 'Crop type (e.g. maize)'),
                validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _sizeController,
                decoration: const InputDecoration(labelText: 'Size (acres, optional)'),
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
              ),
              const SizedBox(height: 12),
              zonesAsync.when(
                loading: () => const LinearProgressIndicator(),
                error: (e, _) => Text('Could not load zones: $e'),
                data: (zones) => DropdownButtonFormField<String>(
                  initialValue: _selectedZoneCode,
                  decoration: const InputDecoration(labelText: 'District / zone'),
                  items: zones
                      .map((z) => DropdownMenuItem(value: z.code, child: Text(z.name)))
                      .toList(),
                  onChanged: (value) => setState(() => _selectedZoneCode = value),
                ),
              ),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: _submitting ? null : _submit,
                child: _submitting
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : const Text('Save farm'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
