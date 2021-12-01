import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import injectContext from './store/appContext';
import Home from './views/Home';
import Login from './views/Login';

const Layout = () => {
    return (
        <BrowserRouter>
            <Switch>
                <Route exact path="/login" component={Login} />
                <Route exact path="/" component={Home} />
            </Switch>
        </BrowserRouter>
    )
}

export default injectContext(Layout);