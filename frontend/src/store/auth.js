// check if user is log in or not using zustand 
// if value is null i.e no login user else user is login so we store it

import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";
//this is zostand store for user Info
const userAuthStore = create((set,get)=>({
    //user data varibale 
    allUserData : null, //when no user 
    loading : false,
    
    user:()=>({
        user_id:get().allUserData.user_id||null,
        username:get().allUserData.username||null,
    }),

    setUser:(user)=>set({
        allUserData:user
    }),

    setloading:(loading)=>({loading}),

    isLoggedIn:()=>get().allUserData !== null,
}))

//you can create more store as you can 

// const ProfileStore = create((set,get)=>{

// })
if (import.meta.env.DEV){
    mountStoreDevtool("store",userAuthStore)
}
//import devtool only when we run on develoment
export {userAuthStore}