// React
import React, { useState, useEffect } from 'react';
import {
  View,
  Image,
  Text,
  TextInput,
  Alert,
  Pressable,
  ScrollView,
} from 'react-native';
import { FlatGrid } from 'react-native-super-grid';
import { Dialog } from 'react-native-paper';

// Icon
import Icon from 'react-native-vector-icons/Ionicons';

// API
import ApiManager from '../../../config/instance';

// Custom Styled
import { styled } from 'nativewind';

// Navigation
import { useNavigation } from '@react-navigation/native';

// Poppins Fonts
import {
  useFonts,
  Poppins_100Thin,
  Poppins_100Thin_Italic,
  Poppins_200ExtraLight,
  Poppins_200ExtraLight_Italic,
  Poppins_300Light,
  Poppins_300Light_Italic,
  Poppins_400Regular,
  Poppins_400Regular_Italic,
  Poppins_500Medium,
  Poppins_500Medium_Italic,
  Poppins_600SemiBold,
  Poppins_600SemiBold_Italic,
  Poppins_700Bold,
  Poppins_700Bold_Italic,
  Poppins_800ExtraBold,
  Poppins_800ExtraBold_Italic,
  Poppins_900Black,
  Poppins_900Black_Italic,
} from '@expo-google-fonts/poppins';

// Bottom Tabs
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { RetreiveData } from '../../storage/Storage';

// Styled
const StyledView = styled(View);
const StyledImage = styled(Image);

// Images & Icons
const waveBG = require('../../../assets/images/wave.png');
const studentBG = require('../../../assets/images/student-bg.png');

// Icons
const emptyIcon = require('../../../assets/icons/empty.png');
const scolaIcon = require('../../../assets/icons/icon.png');
const attendanceIcon = require('../../../assets/icons/attendance.png');
const calendarIcon = require('../../../assets/icons/calendar.png');
const taskIcon = require('../../../assets/icons/tasks.png');
const assessmentIcon = require('../../../assets/icons/assessment.png');
const studentIcon = require('../../../assets/icons/student.png');
const settingIcon = require('../../../assets/icons/setting.png');

// Self Icon
const selfAttendanceIcon = require('../../../assets/icons/self-attendance.png');

const HomeStack = () => {
  const navigation = useNavigation();
  /* Setup Icon */
  let [fontsLoaded] = useFonts({
    Poppins_100Thin,
    Poppins_100Thin_Italic,
    Poppins_200ExtraLight,
    Poppins_200ExtraLight_Italic,
    Poppins_300Light,
    Poppins_300Light_Italic,
    Poppins_400Regular,
    Poppins_400Regular_Italic,
    Poppins_500Medium,
    Poppins_500Medium_Italic,
    Poppins_600SemiBold,
    Poppins_600SemiBold_Italic,
    Poppins_700Bold,
    Poppins_700Bold_Italic,
    Poppins_800ExtraBold,
    Poppins_800ExtraBold_Italic,
    Poppins_900Black,
    Poppins_900Black_Italic,
  });

  /* Navigation Menu */

  // Absence
  const absenceView = () => {
    Alert.alert('Absence Coming soon.');
  };

  // Attendance
  const attendanceView = () => {
    navigation.navigate('AttendanceFacultyPage');
  };

  /* Menus */
  const [items] = React.useState([
    { name: 'Kehadiran', icon: attendanceIcon, view: attendanceView },
    { name: 'Jadwal', icon: calendarIcon },
    { name: 'Tugas', icon: taskIcon },
    { name: 'Penilaian', icon: assessmentIcon },
    { name: 'Siswa', icon: studentIcon },
    { name: 'Pengaturan', icon: settingIcon },
  ]);

  // State Management
  const [teacherName, setTeacherName] = useState();

  const getTeacherName = async () => {
    try {
      const name = await RetreiveData('as_teacher_name');
      if (name != null) {
        setTeacherName(name);
      } else {
        setTeacherName(`Undefined`);
      }
    } catch (err) {
      console.log(`Error : ${err}`);
    }
  };

  useEffect(() => {
    getTeacherName();
  });

  if (!fontsLoaded) {
    return <Text>Loading...</Text>;
  } else {
    return (
      <ScrollView className="bg-blue-900 h-full">
        <Image source={waveBG} className="max-w-full h-80 absolute"></Image>

        <Image
          source={studentBG}
          className="max-w-full absolute h-40 bottom-0"
        ></Image>

        <StyledView>
          <StyledView className="m-4 mt-16 mb-12 flex flex-row justify-between">
            <StyledView>
              <Image source={scolaIcon} className="h-14 w-14"></Image>
              <StyledView className="flex flex-col">
                <StyledView className="flex flex-row gap-1">
                  <Text
                    className="text-lg"
                    style={{
                      fontFamily: 'Poppins_500Medium',
                    }}
                  >
                    Selamat
                  </Text>
                  <Text
                    className="text-lg text-blue-900"
                    style={{
                      fontFamily: 'Poppins_500Medium',
                    }}
                  >
                    Datang,
                  </Text>
                </StyledView>
                <Text style={{ fontFamily: 'Poppins_400Regular' }}>
                  {teacherName ? teacherName : `Undefined`}
                </Text>
              </StyledView>
            </StyledView>
            <Pressable
              onPress={absenceView}
              className="items-center justify-center bg-white shadow-lg shadow-black rounded-lg px-7 active:bg-gray-100"
            >
              <Image source={selfAttendanceIcon} className="h-14 w-14"></Image>
              <StyledView className="flex flex-col">
                <StyledView className="flex flex-row gap-1 justify-center items-center">
                  <Text
                    style={{
                      fontFamily: 'Poppins_500Medium',
                    }}
                  >
                    Absen
                  </Text>
                </StyledView>
              </StyledView>
            </Pressable>
          </StyledView>

          <StyledView className="items-center justify-center p-2 bg-gray-50 shadow-lg shadow-black rounded-lg mx-4">
            <Text
              className="text-xl self-start m-2 text-blue-900"
              style={{ fontFamily: 'Poppins_700Bold' }}
            >
              Menu
            </Text>
            <FlatGrid
              itemDimension={90}
              data={items}
              spacing={12}
              scrollEnabled={false}
              renderItem={({ item }) => (
                <View className="p-2">
                  <Pressable
                    className="items-center justify-center border border-transparent active:bg-gray-100 active:border active:border-gray-200 active:rounded-lg"
                    onPress={item.view}
                  >
                    <Image
                      source={item.icon}
                      className="h-10 w-10 flex"
                    ></Image>
                    <Text
                      className="text-center text-xs mt-1 text-gray-900"
                      style={{
                        fontFamily: 'Poppins_500Medium',
                      }}
                    >
                      {item.name}
                    </Text>
                  </Pressable>
                </View>
              )}
            />
          </StyledView>
        </StyledView>

        <StyledView className="h-80 mx-4 my-10 bg-white shadow-lg shadow-black rounded-lg">
          <Text
            className="text-xl self-start text-blue-900 mx-4 mt-4"
            style={{ fontFamily: 'Poppins_700Bold' }}
          >
            Jadwal
          </Text>
          <StyledView className="flex justify-center items-center my-auto">
            <StyledImage source={emptyIcon} className="h-24 w-24"></StyledImage>
            <Text className="text-blue-500 font-bold">
              Data tidak ditemukan
            </Text>
          </StyledView>
        </StyledView>
      </ScrollView>
    );
  }
};

const ArchiveStack = () => {
  return (
    <StyledView>
      <Text>Archive</Text>
    </StyledView>
  );
};

const LogoutStack = () => {
  const [visible, setVisible] = React.useState(false);

  const hideDialog = () => setVisible(false);

  return (
    <StyledView>
      <Text></Text>
      <Dialog visible={visible} onDismiss={hideDialog}>
        <Dialog.Icon icon="alert" />
        <Dialog.Title>This is a title</Dialog.Title>
        <Dialog.Content>
          <Text variant="bodyMedium">This is simple dialog</Text>
        </Dialog.Content>
      </Dialog>
    </StyledView>
  );
};

export const TabHome = () => {
  const Tab = createBottomTabNavigator();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Beranda') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Pesan') {
            iconName = focused ? 'mail' : 'mail-outline';
          } else if (route.name === 'Pengaturan') {
            iconName = focused ? 'settings' : 'settings-outline';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#1e3a8a',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen
        name="Beranda"
        component={HomeStack}
        options={{
          headerLeft: null,
          headerBackVisible: false,
          headerShown: false,
        }}
      />
      <Tab.Screen
        name="Pesan"
        component={ArchiveStack}
        options={{
          headerLeft: null,
          headerBackVisible: false,
          headerShown: false,
        }}
      />
      <Tab.Screen
        name="Pengaturan"
        component={LogoutStack}
        options={{
          headerLeft: null,
          headerBackVisible: false,
          headerShown: false,
        }}
      />
    </Tab.Navigator>
  );
};
