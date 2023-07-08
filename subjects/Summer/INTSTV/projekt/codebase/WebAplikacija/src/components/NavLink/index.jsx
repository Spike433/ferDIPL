import { memo } from "react";
import { useNavigate } from "react-router-dom";

import styles from './NavLink.module.css';

const NavLink = (props) => {
    const { label, to } = props;
    const navigate = useNavigate();


    return (
        <div onClick={() => navigate(to)} className={styles.label}>
            {label}
        </div>
    )
}

export default memo(NavLink);