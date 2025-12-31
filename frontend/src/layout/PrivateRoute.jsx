import { Navigate } from "react-router-dom";
import {userAuthStore} from '../store/auth'

const PrivateRoute = ({children}) =>{
    const isLoggedIn = userAuthStore((state)=> state.isLoggedIn)()//this is zostand store

    return isLoggedIn?<>{children}</> : <Navigate to={"/login"} />
}
export default PrivateRoute
{/* <Navigate to='login/'/> */}

//so now any private route we wrapp into this

{/* <PrivateRoute>
    </adminDashbord>
</PrivateRoute> */}