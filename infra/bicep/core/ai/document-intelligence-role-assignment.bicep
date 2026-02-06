// Document Intelligence Role Assignment for Container App Managed Identity
// Assigns Cognitive Services User role to allow Document Intelligence API calls

@description('Document Intelligence account name')
param documentIntelligenceAccountName string

@description('Principal ID of the managed identity (from Container App)')
param principalId string

// Cognitive Services User - allows calling Cognitive Services APIs including Document Intelligence
var cognitiveServicesUserRoleId = 'a97b65f3-24c7-4388-baec-2e87135dc908'

// Reference existing Document Intelligence account
resource documentIntelligenceAccount 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' existing = {
  name: documentIntelligenceAccountName
}

// Assign Cognitive Services User role to the managed identity
resource documentIntelligenceRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(documentIntelligenceAccount.id, principalId, cognitiveServicesUserRoleId)
  scope: documentIntelligenceAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesUserRoleId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
