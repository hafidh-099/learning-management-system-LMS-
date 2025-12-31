import {userAuthStore} from '../store/auth'
import axios from './axios'
import jwtDecode from 'jwt-decode'
import cookie from 'js-cookie'
import Swal from 'sweetalert2'

export const login = async(email,password)=>{
    try {
        const {data,status} = await axios.post('user/token/access/',{
            email,
            password
        })//this value we accept from user who login
        if (status === 200){
            setAuthUser(data.access,data.refresh) //if user login get access and refresh token
            //set data to cookie and alert user
            alert("login Succefully")
        }
        return {data,error:null};
    } catch (error) {
        console.log(error)
        return {
            data:null,
            error: `${error.response.data.detail}` || "Something went wrong"
        }    
    }
}
export  const register = async(full_name,email,password,password2)=>{
    try {
        const {data,status } = await axios.post('user/register/',{
            full_name,
            email,
            password,
            password2
        });
        //we want to automatic user login in .if you dont want dont put anything
        await login(email,password)
        alert("Registration Successfull")
        return {data,error:null}
    } catch (error) {
        console.log(error)
        // alert(`${error.response.data.full_name} - ${error.response.data.full_name}`)
        return {
            data:null,
            error: `${error.response.data.email} - ${error.response.data.password}` || "Something went wrong"
        }
    }
}
//logout
export const logout = () =>{
    //only we need is to clear cookie
    cookie.remove("access_token")
    cookie.remove("refresh_token")
    userAuthStore.getState().setUser(null)

    alert("You have been logged out")
}

export const setUser=async()=>{
    const access_token = cookie.get('access_token')
    const refresh_token = cookie.get('refresh_token')

    if (!access_token || !refresh_token){
        return ;
    }
    //check if token expired so we refresh and get new
    if (isAccessTokenExpired(access_token)){
        const response = getRefreshedToken(refresh_token);
        setAuthUser(response.access,response.refresh)//recall if we get new token we get new refresh and access
    }else{
        //if not expired
        setAuthUser(access_token,refresh_token)
    }
}

export const setAuthUser =(access_token,refresh_token)=>{
    cookie.set('access_token',access_token,{//Note access_token is cookie key with it value
        expires : 1, //one day(for security reason)
        secure:true
    }),
    cookie.set('refresh_token',refresh_token,{//Note refresh_token is cookie key with it value
        expires : 7, //seven day
        secure:true
    })
    const user = jwtDecode(access_token)??null //if dont exist we pass null

    if(user){
        userAuthStore.getState().setUser(user);
    }else{
        //if user dont exist
        setAuthUser.getState().setLoading(false)
    }
}

//get refresh token
export const getRefreshedToken = async()=>{
    const refresh_token = cookie.get("refresh_token")
    //get refresh token
    const response = await axios.post('user/token/refresh/',{
        refresh:refresh_token,
    })
    return response.data
}

//if access token is expired
export const isAccessTokenExpired=(access_token)=>{
    try {
        const docodedToken = jwtDecode(access_token)
        return docodedToken.exp < Date.now()/1000
    } catch (error) {
        console.log(error)
        return true
    }
}