import React, { useState, useEffect } from 'react';
import { View, Image, Text, TextInput, Keyboard, Pressable, Alert, KeyboardAvoidingView, Platform, ScrollView } from "react-native";
import { KeyboardAvoidingScrollView } from 'react-native-keyboard-avoiding-scroll-view';
import Ionicons from '@expo/vector-icons/Ionicons';

import ApiManager from '../config/instance';
import { styled } from 'nativewind';

const StyledView = styled(View);
const StyledScrollView = styled(KeyboardAvoidingScrollView);

// Logo Scola
const logo = require('../assets/images/scola.png');

// Logout Background
const bg = require('../assets/images/login-bg.png');
const studentBG = require('../assets/images/student-background.png');

export const Logout = ({ navigation }) => {

   const [confirmLogout, setConfirmLogout] = useState(false)

    const handleLogout = async () => {
        try {

            await ApiManager.post('/web/session/authenticate', {
                method: 'POST',
                params: {
                    db: 'scola',
                    login: username,
                    password: password
                },
            }).then(resp => {
                // console.log("resp : ", resp.data['result']);
                console.log("name : ", resp.data['result']['user_settings']);

                if (!resp.data['result']) {
                    
                }
                // console.log("response : ", resp.data['response_detail'].response_code);
                if(username == '' || password == '') {
                    return showAlertMandatory();
                }

                if(resp.data['result']['user_settings']) {
                    navigation.navigate('TabHomeTeacher')
                } else {
                    return showAlertForbidden();
                }

                // if(resp.data['response_detail'].response_code == 403) {
                //     return showAlertForbidden();
                // } else {
                //     navigation.navigate('Home')
                // }


            })
        } catch (error) {
            console.log("error : ", error)
        }

    }

    const handleShowPassword = async (showPassword) => {
        if (showPassword) {
            setShowPassword(false)
        } else {
            setShowPassword(true);
        }
    }

    /* Alert List */
    const showAlertForbidden = () => {
        Alert.alert(
            "Login Gagal",
            "Email atau password salah.", // Description text
            [
                {
                    text: "Tutup",
                    onPress: () => console.log("Oke pressed"),
                    style: "default", // Optional style, could be "default", "cancel", or "destructive"
                }
            ],
            { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
        );
    }

    const showAlertMandatory = () => {
        Alert.alert(
            "Perhatian", // Title of the alert
            "Email dan password tidak boleh kosong.", // Description text
            [
                {
                    text: "Tutup", // Button text
                    onPress: () => console.log("Oke pressed"), // Optional callback when button is pressed
                    style: "default", // Optional style, could be "default", "cancel", or "destructive"
                }
            ],
            { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
        );
    }

    const showAlertSuccess = () => {
        Alert.alert(
            "Sukses", // Title of the alert
            "Berhasil melakukan login.", // Description text
            [
                {
                    text: "Tutup", // Button text
                    onPress: () => console.log("Oke pressed"), // Optional callback when button is pressed
                    style: "default", // Optional style, could be "default", "cancel", or "destructive"
                }
            ],
            { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
        );
    }

    return (
        <StyledScrollView className="bg-blue-900">
            <Image source={bg} className='absolute max-w-full' style={{ height: '80%' }}></Image>
            <Image source={studentBG} className='absolute bottom-0 max-w-full' style={{ height: '30%' }}></Image>
            <StyledView className='flex-1 top-24 h-screen mb-16'>
                <StyledView>
                    <Image source={logo} className='w-screen h-28'></Image>
                    <Text className="text-center text-2xl text-blue-900 my-7 font-bold">Login</Text>
                    <StyledView className='mx-16'>
                        <TextInput
                            className="border rounded-xl px-4 py-1"
                            placeholder="Email"
                            onChangeText={setUsername}
                            value={username}
                            autoCapitalize='none'
                            keyboardType='email-address'
                        />
                        {
                            showPassword ?
                                <StyledView className="w-full border rounded-xl mt-4 py-1">
                                    <StyledView className='flex flex-row'>
                                        <TextInput
                                            className="flex px-4 w-full"
                                            placeholder="Password"
                                            onChangeText={setPassword}
                                            value={password}
                                            secureTextEntry={false}
                                            autoCapitalize='none'
                                        />
                                        <Pressable onPress={() => handleShowPassword(showPassword)} className="ml-2 absolute right-0 mr-2">
                                            <Ionicons name="eye-off-outline" size={24} color="black" className="self-center" />
                                        </Pressable>
                                    </StyledView>
                                </StyledView>
                                :
                                <StyledView className="w-full border rounded-xl mt-4 py-1">
                                    <StyledView className='flex flex-row'>
                                        <TextInput
                                            className="flex px-4 w-full"
                                            placeholder="Password"
                                            onChangeText={setPassword}
                                            value={password}
                                            secureTextEntry={true}
                                            autoCapitalize='none'
                                        />
                                        <Pressable onPress={() => handleShowPassword(showPassword)} className="ml-2 absolute right-0 mr-2">
                                            <Ionicons name="eye-outline" size={24} color="black" className="self-center" />
                                        </Pressable>
                                    </StyledView>
                                </StyledView>
                        }
                    </StyledView>

                    <StyledView className="mt-10 flex justify-items-center items-center">
                        <Pressable onPress={() => handleLogin()

                        } className="border border-blue-900 px-10 py-2.5 rounded-full bg-blue-900 active:bg-blue-800">
                            <Text className="font-medium text-white hover:text-black">Login</Text>
                        </Pressable>
                    </StyledView>

                </StyledView>

            </StyledView>


        </StyledScrollView>

    )
}