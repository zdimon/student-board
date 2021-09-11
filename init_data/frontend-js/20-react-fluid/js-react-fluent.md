# React фреймворк Fluent.

[ссылка на сайт](https://developer.microsoft.com/en-us/fluentui#/)

Быстрый старт проекта.

    npx create-react-app fluent --template typescript
    

Установка либы.

    npm install @fluentui/react --save 
    npm install office-ui-fabric-react --save 

## Выводим кнопки.

    import React from 'react';адгуте
    import logo from './logo.svg';
    import './App.css';
    import { DefaultButton, PrimaryButton, Stack, IStackTokens } from 'office-ui-fabric-react';

    function App(props: any) {
      return (
        <div className="App">
          <Stack horizontal>
            <DefaultButton text="Standard" onClick={_alertClicked} allowDisabledFocus disabled={props.disabled} checked={props.checked} />
            <PrimaryButton text="Primary" onClick={_alertClicked} allowDisabledFocus disabled={props.disabled} checked={props.checked} />
        </Stack>
        </div>
      );
    }

    function _alertClicked(): void {
      alert('Clicked');
    }

    export default App;

![start page]({path-to-subject}/images/2.png)

Изменяем цвет.

    <PrimaryButton style={{ backgroundColor: '#FE0000' }} text="Primary" />

## Кнопки с меню и иконками.

Включаем иконки в src/index.tsx

    import { initializeIcons } from '@uifabric/icons';
    initializeIcons();

Импортируем интерфейсы и применям.

    import { CommandBarButton, IIconProps, IContextualMenuProps } from 'office-ui-fabric-react';



    function App(props: any) {
      const addIcon: IIconProps = { iconName: 'Add' };
      const mailIcon: IIconProps = { iconName: 'Mail' };
      const menuProps: IContextualMenuProps = {
        items: [
          {
            key: 'emailMessage',
            text: 'Email message',
            iconProps: { iconName: 'Mail' },
          },
          {
            key: 'calendarEvent',
            text: 'Calendar event',
            iconProps: { iconName: 'Calendar' },
          },
        ],
      };
      return (
        <div className="App">
        ...

        <div className="ms-Grid-row">
            <div className="ms-Grid-col">
            <CommandBarButton
                iconProps={addIcon}
                text="New item"
                menuProps={menuProps}
                disabled={props.disabled}
                checked={props.checked}
              />
            </div>
        </div>

        ...

![start page]({path-to-subject}/images/3.png)

Кнопка с меню

          <DefaultButton
          text="Primary"
          primary
          split
          splitButtonAriaLabel="See 2 options"
          aria-roledescription="split button"
          menuProps={menuProps}
          onClick={_alertClicked}
          disabled={props.disabled}
          checked={props.checked}
        />

![start page]({path-to-subject}/images/4.png)

[дока по кнопкам](https://developer.microsoft.com/en-us/fluentui#/controls/web/button)

    

### Прикручиваем систему гридов.

Вставим слили в public/index.html


        <link
      rel="stylesheet"
      href="https://static2.sharepointonline.com/files/fabric/office-ui-fabric-core/11.0.0/css/fabric.min.css"
        />


Пример грида.

    <div className="ms-Grid" dir="ltr">
      <div className="ms-Grid-row">
        <div className="ms-Grid-col ms-sm6 ms-md4 ms-lg2">
          <DefaultButton text="Standard" allowDisabledFocus />
        </div>
        <div className="ms-Grid-col ms-sm6 ms-md8 ms-lg10">
          <DefaultButton text="Standard" allowDisabledFocus />
        </div>
      </div>
    </div>

[ссылка на документацию](https://developer.microsoft.com/en-us/fluentui#/styles/web/layout)


## Строка навигации CommandBar.

    ...

    import { CommandBar, ICommandBarItemProps } from 'office-ui-fabric-react/lib/CommandBar';
    import { IButtonProps } from 'office-ui-fabric-react/lib/Button';



    function App(props: any) {
     

      const _items: ICommandBarItemProps[] = [
        {
          key: 'newItem',
          text: 'New',
          cacheKey: 'myCacheKey', // changing this key will invalidate this item's cache
          iconProps: { iconName: 'Add' },
          subMenuProps: {
            items: [
              {
                key: 'emailMessage',
                text: 'Email message',
                iconProps: { iconName: 'Mail' },
                ['data-automation-id']: 'newEmailButton', // optional
              },
              {
                key: 'calendarEvent',
                text: 'Calendar event',
                iconProps: { iconName: 'Calendar' },
              },
            ],
          },
        },
        {
          key: 'upload',
          text: 'Upload',
          iconProps: { iconName: 'Upload' },
          href: 'https://developer.microsoft.com/en-us/fluentui',
        },
        {
          key: 'share',
          text: 'Share',
          iconProps: { iconName: 'Share' },
          onClick: () => console.log('Share'),
        },
        {
          key: 'download',
          text: 'Download',
          iconProps: { iconName: 'Download' },
          onClick: () => console.log('Download'),
        },
      ];

      const _overflowItems: ICommandBarItemProps[] = [
        { key: 'move', text: 'Move to...', onClick: () => console.log('Move to'), iconProps: { iconName: 'MoveToFolder' } },
        { key: 'copy', text: 'Copy to...', onClick: () => console.log('Copy to'), iconProps: { iconName: 'Copy' } },
        { key: 'rename', text: 'Rename...', onClick: () => console.log('Rename'), iconProps: { iconName: 'Edit' } },
      ];
      const overflowProps: IButtonProps = { ariaLabel: 'More commands' };

      const _farItems: ICommandBarItemProps[] = [
        {
          key: 'tile',
          text: 'Grid view',
          // This needs an ariaLabel since it's icon-only
          ariaLabel: 'Grid view',
          iconOnly: true,
          iconProps: { iconName: 'Tiles' },
          onClick: () => console.log('Tiles'),
        },
        {
          key: 'info',
          text: 'Info',
          // This needs an ariaLabel since it's icon-only
          ariaLabel: 'Info',
          iconOnly: true,
          iconProps: { iconName: 'Info' },
          onClick: () => console.log('Info'),
        },
      ];
    return (
        <div className="App">
          
          <CommandBar
            items={_items}
            overflowItems={_overflowItems}
            overflowButtonProps={overflowProps}
            farItems={_farItems}
            ariaLabel="Use left and right arrow keys to navigate between commands"
          /> 
        </div>

       
      );
    }

![start page]({path-to-subject}/images/5.png)

## Строка навигации Pivot.

        import { PivotItem, IPivotItemProps, Pivot } from 'office-ui-fabric-react/lib/Pivot';
        import { Icon } from 'office-ui-fabric-react/lib/Icon';
        import { Label, ILabelStyles } from 'office-ui-fabric-react/lib/Label';
        import { IStyleSet } from 'office-ui-fabric-react/lib/Styling';

        function App(props: any) {
          const labelStyles: Partial<IStyleSet<ILabelStyles>> = {
            root: { marginTop: 10 },
          };


          return (
            <div className="App">
              
              <div>
              <Pivot aria-label="Count and Icon Pivot Example">
                <PivotItem headerText="My Files" itemCount={42} itemIcon="Emoji2">
                  <Label styles={labelStyles}>Pivot #1</Label>
                </PivotItem>
                <PivotItem itemCount={23} itemIcon="Recent">
                  <Label styles={labelStyles}>Pivot #2</Label>
                </PivotItem>
                <PivotItem headerText="Placeholder" itemIcon="Globe">
                  <Label styles={labelStyles}>Pivot #3</Label>
                </PivotItem>
                <PivotItem headerText="Shared with me" itemIcon="Ringer" itemCount={1}>
                  <Label styles={labelStyles}>Pivot #4</Label>
                </PivotItem>
                <PivotItem headerText="Customized Rendering" itemIcon="Globe" itemCount={10} >
                  <Label styles={labelStyles}>Customized Rendering</Label>
                </PivotItem>
              </Pivot>
            </div>
            </div>

           
          );
        }

    export default App;

![start page]({path-to-subject}/images/6.png)

