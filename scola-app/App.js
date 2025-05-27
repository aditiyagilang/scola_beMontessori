import { StatusBar } from 'expo-status-bar';
import * as React from 'react';
import { Button, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import { Login } from './src/Login'
import { TabHome } from './src/views/faculty/Home'
import { AttendanceFacultyPage } from './src/views/faculty/pages/attendance/Attendance.jsx'
import { AttendanceSheetPage } from './src/views/faculty/pages/attendance/AttendanceSheet.jsx'


const Stack = createNativeStackNavigator();


export default function App() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Login">
                <Stack.Screen name="Login" component={Login} options={
                    {headerLeft: null, headerBackVisible: false, headerShown: false}
                }/>

                {/* Faculty / Teacher Role */}
                <Stack.Screen name="TabHomeTeacher" component={TabHome} options={
                    {headerLeft: null, headerBackVisible: false, headerShown: false}
                }/>
                <Stack.Screen name="AttendanceFacultyPage" component={AttendanceFacultyPage} options={
                    {headerLeft: null, headerBackVisible: false, headerShown: false}
                }/>
                <Stack.Screen name="AttendanceSheetPage" component={AttendanceSheetPage} options={
                    {headerLeft: null, headerBackVisible: false, headerShown: false}
                }/>
                
            </Stack.Navigator>
        </NavigationContainer>
    );
}