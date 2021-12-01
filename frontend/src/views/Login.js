import React, { useContext } from 'react';
import { useHistory } from 'react-router-dom';
import { Context } from '../store/appContext';

const Login = () => {
    const history = useHistory();
    const { store, actions } = useContext(Context);
    const { currentUser, email, password, error } = store;
    const { loginSubmit, loginChange } = actions;
    if (!!currentUser) history.push('/');

    return (
        <>
            <div className="container">
                <h1>LOGIN</h1>
                <div className="row">
                    <div className="col-md-6 offset-md-3">
                        {!!error && error.faild && (
                            <div className="alert alert-warning" role="alert">
                                {error.faild}
                            </div>
                        )}
                        <form onSubmit={loginSubmit}>
                            <div className="row mb-3">
                                <label htmlFor="inputEmail3" className="col-sm-2 col-form-label">
                                    Email
                                </label>
                                <div className="col-sm-10">
                                    <input type="email" className={"form-control" + (!!error && error.email ? " is-invalid" : "")} name="email" value={email} onChange={loginChange} />
                                    <div className="invalid-feedback">
                                        {!!error && error.email}
                                    </div>
                                </div>
                            </div>
                            <div className="row mb-3">
                                <label htmlFor="inputPassword3" className="col-sm-2 col-form-label">
                                    Password
                                </label>
                                <div className="col-sm-10">
                                    <input type="password" className={"form-control" + (!!error && error.password ? " is-invalid" : "")} name="password" value={password} onChange={loginChange} />
                                    <div className="invalid-feedback">
                                        {!!error && error.password}
                                    </div>
                                </div>
                            </div>
                            <div className="d-grid">
                                <button type="submit" className="btn btn-primary gap-2">
                                    Sign in
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login;