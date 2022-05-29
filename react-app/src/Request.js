import axios from 'axios';
import { config } from './config';

export class Request {
  constructor() {
    if (window.localStorage.getItem('token')) {
      this.config = {
        headers: {
          Authorization: `Token ${window.localStorage.getItem('token')}`,
        },
      };
    } else {
      this.config = {};
    }
  }

  get = async function (url) {
    const response = await axios.get(`${config.serverURL}${url}`);
    return response.data;
  };

  post = async function (url, payload) {
    const response = await axios.post(
      `${config.serverURL}${url}`,
      payload,
      this.config
    );
    return response.data;
  };
}
