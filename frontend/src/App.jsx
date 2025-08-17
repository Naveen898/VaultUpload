import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={UploadPage} />
                <Route path="/login" component={LoginPage} />
                <Route component={NotFoundPage} />
            </Switch>
        </Router>
    );
};

export default App;