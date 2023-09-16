import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String serverResponse = "Awaiting response...";

  void _handleResponse(http.Response response) {
    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      setState(() {
        serverResponse = data['response'].toString();
      });
    } else {
      setState(() {
        serverResponse = "Error with request: ${response.statusCode}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('My Chatbot App')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () async {
                var response = await http.post(
                  Uri.parse('http://localhost:5000/plan_trip'),
                  body: jsonEncode({'user_input': 'When is the next bus?'}),
                  headers: {'Content-Type': 'application/json'},
                );
                _handleResponse(response);
              },
              child: Text('Plan Trip'),
            ),
            ElevatedButton(
              onPressed: () async {
                var response = await http.post(
                  Uri.parse('http://localhost:5000/nearest_stop'),
                  body: jsonEncode({'latitude': 40.7128, 'longitude': -74.0060}),
                  headers: {'Content-Type': 'application/json'},
                );
                _handleResponse(response);
              },
              child: Text('Find Nearest Stop'),
            ),
            ElevatedButton(
              onPressed: () async {
                var response = await http.post(
                  Uri.parse('http://localhost:5000/fare_info'),
                  body: jsonEncode({'user_input': 'adult'}),
                  headers: {'Content-Type': 'application/json'},
                );
                _handleResponse(response);
              },
              child: Text('Check Adult Fare'),
            ),
            SizedBox(height: 20),
            Text('Server Response: $serverResponse'),
          ],
        ),
      ),
    );
  }
}
