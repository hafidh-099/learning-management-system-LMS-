//we want to check user api. if expire we give him new token. so we need to intecept the 
// when we make private route this will be called

import axios from "axios";
import {getRefreshedToken,isAccessTokenExpired,setAuthUser} from './auth'
import {API_BASE_URL} from './constant'
import cookie from 'js-cookie'

const useAxios=()=>{
    const accessToken = cookie.get("access_token")
    const refreshToken = cookie.get("refresh_token")

    const axiosInstance = axios.create({
        baseURL:API_BASE_URL,
        headers:{Authorization:`Bearer ${accessToken}`}      
    });

    axiosInstance.interceptors.request.use(async(req)=>{
        if(!isAccessTokenExpired){
            return req
        }else{
            //if expire
            const response = await getRefreshedToken(refreshToken)
            setAuthUser(response.access,response.refresh)
            response.headers.Authorization = `Bearer ${response.data?.access}`
        }
    });
    return axiosInstance
}

export default useAxios