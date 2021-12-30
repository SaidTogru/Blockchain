import { Injectable } from '@angular/core';

const USER_KEY = 'auth-user';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  constructor() { }

  public saveUser(user: string) {
    window.sessionStorage.removeItem(USER_KEY);
    window.sessionStorage.setItem(USER_KEY, user);
  }

  public savePort(port: any) {
    window.sessionStorage.removeItem('auth-port');
    window.sessionStorage.setItem('auth-port', port);
  }

  public getUser(): any | null  {
    return sessionStorage.getItem(USER_KEY);
  }

  public getPort(): any | null  {
    return sessionStorage.getItem('auth-port');
  }

}
