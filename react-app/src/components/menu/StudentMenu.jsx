import React, { useEffect } from 'react';
// import PropTypes from 'prop-types';
import { Request } from '../../Request';

// const getLang = function () {
//   const url = window.location.href;
//   console.log(url);
//   const arr = url.split('/')[3];
//   return arr;
// };

export default function StudentMenu() {
  const [courses, setCourses] = React.useState([]);

  useEffect(() => {
    const req = new Request();

    req
      .get('course/list')
      .then(payload => {
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
          href={el.get_student_absolute_url}
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
