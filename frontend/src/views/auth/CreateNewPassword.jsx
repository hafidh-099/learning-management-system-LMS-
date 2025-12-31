import React from 'react'
import BaseHeader from '../partials/BaseHeader'
import BaseFooter from '../partials/BaseFooter'
import apiInstance from '../../utils/axios'
import { useState,useEffect } from 'react'
import { useNavigate,useSearchParams } from 'react-router-dom'

function CreateNewPassword() {
  const [password,setPassword] = useState("")
  const [confirmPassword,setConfirmPassword] = useState("")
  const [isloading,setisLoading] = useState(false)

  const navigate = useNavigate()
  const [seachParam] = useSearchParams()
  const otp = seachParam.get('otp')
  const uuidb64 = seachParam.get('uuidb64')
  const refresh_token = seachParam.get('refresh_token')
  
  const handleCreatePassword=async(e)=>{
    setisLoading(false)
    e.preventDefault()
    console.log('password is reset')
    if(password != confirmPassword){
      alert("password not match")
    }else{
      //note we need value from url
      const formData = new FormData()
      formData.append('otp',otp)//take key and value
      formData.append('uuidb64',uuidb64)
      formData.append('refresh_token',refresh_token)
      //note:backend expect password too
      formData.append('password',password)
      //send to backend
      try {
        setisLoading(true)
        await apiInstance.post(`user/password-change/`,formData).then((resp)=>{
          alert(resp.data.message)
        navigate('/login/')
        })
        
      } catch (error) {
        setisLoading(false)
        console.log(error)
      }
    }
  }
  return (
    <>
      <BaseHeader />

      <section className="container d-flex flex-column vh-100" style={{ marginTop: "150px" }}>
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Create New Password</h1>
                  <span>
                    Choose a new password for your account
                  </span>
                </div>
                <form className="needs-validation" noValidate="" onSubmit={handleCreatePassword}>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Enter New Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e)=>setPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid password.
                    </div>
                  </div>


                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e)=>setConfirmPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid password.
                    </div>
                  </div>

                  <div>
                    <div className="d-grid">
                        {isloading ===true && (
                        <button type="submit" className="btn btn-primary">
                        Processing <i className='fas fa-spinner fa-spin'></i>
                      </button>
                      )}
                      {isloading ===false && (
                        <button type="submit" className="btn btn-primary">
                        Save New Password <i className='fas fa-check-circle'></i>
                      </button>
                      )}
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  )
}

export default CreateNewPassword