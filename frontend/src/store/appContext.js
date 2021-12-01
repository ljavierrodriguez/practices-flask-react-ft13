import React, { useEffect, useState } from 'react';
import getState from './flux';

export const Context = React.createContext(null);

const injectContext = PassedComponent => {
    const StoreWrapper = props => {

        const [state, setState] = useState(getState({
            getStore: () => state.store,
            getActions: () => state.actions,
            setStore: updateStore => setState({
                store: Object.assign(state.store, updateStore),
                actions: { ...state.actions }
            })
        }));

        useEffect(() => {
            // Aqui ejecuto actions que se quieran ejecutar al cargar el sitio web
            state.actions.getCurrentUser();
        }, [])


        return (
            <Context.Provider value={state}>
                <PassedComponent {...props} />
            </Context.Provider>
        )
    }

    return StoreWrapper;
}

export default injectContext;