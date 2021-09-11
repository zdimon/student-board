import React, { useEffect } from 'react';
// import PropTypes from 'prop-types';
import { Request } from '../../Request';

export default function StudentMenu() {
  const [courses, setCourses] = React.useState([]);

  useEffect(() => {
    const req = new Request();
    req
      .get('course/list')
      .then(payload => {
        console.log(payload);
        setCourses(payload);
      })
      .catch(() => {});
  }, []);

  return (
    <>
      {courses.map(el => (
        <a
          key={el.id}
          className="nav-link collapsed"
          href="#"
          data-toggle="collapse"
          data-target="#collapseTwo"
          aria-expanded="true"
          aria-controls="collapseTwo"
        >
          <i className="fas fa-fw fa-list-alt"></i>
          <span>{el.name}</span>
        </a>
      ))}
    </>
  );
}
// HelloWorld.propTypes = {
//   title: PropTypes.string,
// };
