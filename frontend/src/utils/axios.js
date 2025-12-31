import axios from "axios";
import {API_BASE_URL} from "./constant"

const apiInstance = axios.create({
    baseURL:API_BASE_URL, 
    //At what time we want to fetch data .if data given not give result it will terminate
    timeout:5000,
    headers:{
        "Content-Type":"application/json",
        Accept:"application/json"
    }
})
export default apiInstance