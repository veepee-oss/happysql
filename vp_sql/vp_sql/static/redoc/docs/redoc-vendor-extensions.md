# ReDoc vendor extensions
ReDoc makes use of the following [vendor extensions](http://swagger.io/specification/#vendorExtensions)

### Swagger Object vendor extensions
Extend OpenAPI root [Swagger Object](http://swagger.io/specification/#swaggerObject)
#### x-servers
Backported from OpenAPI 3.0 [`servers`](https://github.com/OAI/OpenAPI-Specification/blob/OpenAPI.next/versions/3.0.md#server-object). Currently doesn't support templates.

#### x-tagGroups

| Field Name     |	Type	       | Description |
| :------------- | :-----------: | :---------- |
| x-tagGroups         | [ [Tag Group Object](#tagGroupObject) ] | A list of tag groups |

###### Usage in Redoc
`x-tagGroups` is used to group tags in the side menu.
If you are going to use `x-tagGroups`, please make sure you **add all tags to a group**, since a tag that is not in a group, **will not be displayed** at all!

#### <a name="tagGroupObject"></a>Tag Group Object
Information about tags group
###### Fixed fields
| Field Name  |	Type	     | Description |
| :---------- | :--------: | :---------- |
| name        | string     | The group name |
| tags        | [ string ] | List of tags to include in this group

###### x-tagGroups example
json
```json
{
  "x-tagGroups": [
    {
      "name": "User Management",
      "tags": ["Users", "API keys", "Admin"]
    },
    {
      "name": "Statistics",
      "tags": ["Main Stats", "Secondary Stats"]
    }
  ]
}
```
yaml
```yaml
x-tagGroups:
  - name: User Management
    tags:
      - Users
      - API keys
      - Admin
  - name: Statistics
    tags:
      - Main Stats
      - Secondary Stats
```

#### <a name="logoObject"></a>Logo Object

### Info Object vendor extensions
Extends OpenAPI [Info Object](http://swagger.io/specification/#infoObject)
#### x-logo

| Field Name     |	Type	       | Description |
| :------------- | :-----------: | :---------- |
| x-logo         | [Logo Object](#logoObject)  | The information about API logo |

###### Usage in Redoc
`x-logo` is used to specify API logo. The corresponding image are displayed just above side-menu.

#### <a name="logoObject"></a>Logo Object
The information about API logo
###### Fixed fields
| Field Name      |	Type	   | Description |
| :-------------- | :------: | :---------- |
| url             | string   | The URL pointing to the spec logo. MUST be in the format of a URL
| backgroundColor | string   | background color to be used. MUST be RGB color in [hexadecimal format] (https://en.wikipedia.org/wiki/Web_colors#Hex_triplet)


###### x-logo example
json
```json
{
  "info": {
    "version": "1.0.0",
    "title": "Swagger Petstore",
    "x-logo": {
      "url": "https://rebilly.github.io/ReDoc/petstore-logo.png",
      "backgroundColor": "#FFFFFF"
    }
  }
}
```
yaml
```yaml
info:
  version: "1.0.0"
  title: "Swagger Petstore"
  x-logo:
    url: "https://rebilly.github.io/ReDoc/petstore-logo.png"
    backgroundColor: "#FFFFFF"
```



### Tag Object vendor extensions
Extends OpenAPI [Tag Object](http://swagger.io/specification/#tagObject)
#### x-traitTag
| Field Name     |	Type	  | Description |
| :------------- | :------: | :---------- |
| x-traitTag     | boolean  | In Swagger two operations can have multiply tags. This property distinguish between tags that are used to group operations (default) from tags that are used to mark operation with certain trait (`true` value) |

#### x-displayName

| Field Name     |	Type	  | Description |
| :------------- | :------: | :---------- |
| x-displayName  | string   | Define the text that is used for this tag in the menu and in section headings |


###### Usage in Redoc
Tags that have `x-traitTag` set to `true` are listed in side-menu but don't have any subitems (operations). Tag `description` is rendered as well.
This is useful for handling out common things like Pagination, Rate-Limits, etc.

###### x-traitTag example
json
```json
{
    "name": "Pagination",
    "description": "Pagination description (can use markdown syntax)",
    "x-traitTag": true
}
```
yaml
```yaml
name: Pagination
description: Pagination description (can use markdown syntax)
x-traitTag: true
```

### Operation Object vendor extensions
Extends OpenAPI [Operation Object](http://swagger.io/specification/#operationObject)
#### x-code-samples
| Field Name     |	Type	  | Description |
| :------------- | :------: | :---------- |
| x-code-samples | [ [Code Sample Object](#codeSampleObject) ]  | A list of code samples associated with operation |

###### Usage in ReDoc
`x-code-samples` are rendered on the right panel of ReDoc

#### <a name="codeSampleObject"></a>Code Sample Object
Operation code sample
###### Fixed fields
| Field Name  |	Type	   | Description  |
| :---------- | :------: | :----------- |
| lang        | string   | Code sample language. Value should be one of the following [list](https://github.com/github/linguist/blob/master/lib/linguist/popular.yml) |
| source      | string   | Code sample source code |


###### Code Sample Object example
json
```json
{
  "lang": "JavaScript",
  "source": "console.log('Hello World');"
}
```
yaml
```yaml
lang: JavaScript
source: console.log('Hello World');
```

### Parameter Object vendor extensions
Extends OpenAPI [Parameter Object](http://swagger.io/specification/#parameterObject)
#### x-examples
| Field Name     |  Type    | Description |
| :------------- | :------: | :---------- |
| x-examples | [Example Object](http://swagger.io/specification/#exampleObject)  | Object that contains examples for the request. Applies when `in` is `body` and mime-type is `application/json` |

###### Usage in ReDoc
`x-examples` are rendered in the JSON tab on the right panel of ReDoc.


### Schema Object vendor extensions
Extends OpenAPI [Schema Object](http://swagger.io/specification/#schemaObject)
#### x-nullable
| Field Name     |	Type	  | Description |
| :------------- | :------: | :---------- |
| x-nullable | boolean | marks schema as a nullable |

###### Usage in ReDoc
Schemas marked as `x-nullable` are marked in ReDoc with the label Nullable

#### x-extendedDiscriminator
**ATTENTION**: This is ReDoc-specific vendor extension. It won't be supported by other tools.

| Field Name     |	Type	  | Description |
| :------------- | :------: | :---------- |
| x-extendedDiscriminator | string | specifies extended discriminator |

###### Usage in ReDoc
ReDoc uses this vendor extension to solve name-clash issues with the standard `discriminator`.
Value of this field specifies the field which will be used as a extended discriminator.
ReDoc displays definition with selectpicker using which user can select value of the `x-extendedDiscriminator`-marked field.
ReDoc displays the definition which is derived from the current (using `allOf`) and has `enum` with only one value which is the same as the selected value of the field specified as `x-extendedDiscriminator`.

###### x-extendedDiscriminator example

```yaml

Payment:
  x-extendedDiscriminator: type
  type: object
  required:
    - type
  properties:
    type:
      type: string
    name:
      type: string

CashPayment:
  allOf:
    - $ref: "#/definitions/Payment"
    - properties:
        type:
          type: string
          enum:
            - cash
        currency:
          type: string

PayPalPayment:
  allOf:
    - $ref: "#/definitions/Payment"
    - properties:
        type:
          type: string
          enum:
            - paypal
        userEmail:
          type: string
```

In the example above the names of definitions (`PayPalPayment`) are named differently than
names in the payload (`paypal`) which is not supported by default `discriminator`.
