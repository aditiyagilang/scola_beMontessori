import 'package:flutter/material.dart';

class StudentPage extends StatelessWidget {
  const StudentPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text(
            "Siswa",
            style: TextStyle(color: Colors.white, fontSize: 20.0),
          ),
          
          actions: [
            Container(
              margin: const EdgeInsets.only(
                  right: 10.0), // Add margin to position the button correctly
              decoration: const BoxDecoration(
                color: Colors.black, // Background color of the button
                shape: BoxShape.circle,
              ),
              child: IconButton(
                icon: const Icon(Icons.manage_accounts),
                color: Colors.white, // Icon color
                onPressed: () {
                  // Your onPressed function here
                },
              ),
            ),
          ],
        ),
        body: GridView.count(
          crossAxisCount: 3,
          children: [
            Container(
              margin: const EdgeInsets.all(10.0),
              padding: const EdgeInsets.all(15.0),
              decoration: BoxDecoration(
                  color: const Color.fromRGBO(255, 255, 255, 1),
                  border:
                      Border.all(color: const Color.fromRGBO(255, 255, 255, 1)),
                  borderRadius: const BorderRadius.all(Radius.circular(10)),
                  boxShadow: const [
                    BoxShadow(
                        color: Color.fromRGBO(0, 33, 71, 0.4),
                        offset: Offset(0, 2),
                        blurRadius: 3,
                        spreadRadius: 0)
                  ]),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/images/students.png',
                    width: 35,
                  ),
                  Container(
                    margin: const EdgeInsets.only(
                        top: 12.0), // Add space between the image and the text
                    child: const Text('Siswa',
                        style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                            color: Color.fromRGBO(0, 33, 71, 1))),
                  ),
                ],
              ),
            )
          ],
        ));
  }
}
