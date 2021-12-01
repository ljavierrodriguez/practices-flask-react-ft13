import React, { useContext, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { Context } from '../store/appContext';
import { FaEdit, FaTrash } from 'react-icons/fa';

const Home = () => {
    const history = useHistory();
    const { store, actions } = useContext(Context);
    const { currentUser, users, error } = store;

    const { getUsers } = actions;

    if (currentUser == null) history.push('/login');

    useEffect(() => {
        if (!!currentUser) getUsers(currentUser.access_token);
    }, [])

    return (
        <>
            <div className="container">
                <h1>HOME</h1>

                <div className="row">
                    <div className="col-md-12">
                        {!!error && error.msg && (
                            <div className="alert alert-warning" role="alert">
                                {error.msg}
                            </div>
                        )}
                        <ul className="list-group">
                            {
                                !!users &&
                                users.map((user, index) => {
                                    return (
                                        <li className="list-group-item" key={index}>
                                            <span className="float-start">{user.email} </span>

                                            {
                                                !!currentUser && currentUser.user.roles.find(role => role.name === "Admin" || role.name === "User") && 
                                                (<span className="float-end mx-2"><FaTrash /></span>)
                                            }

                                            <span className="float-end mx-2"><FaEdit /></span>
                                        </li>
                                    )
                                })
                            }
                        </ul>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Home;